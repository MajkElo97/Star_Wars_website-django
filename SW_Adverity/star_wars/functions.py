import requests
from datetime import datetime as dt
import petl as etl
from .models import DataSet
import os


def get_swapi():
    response = requests.get('https://swapi.dev/api/people/')
    people_dict = response.json()
    people_list = people_dict['results']

    while people_dict['next'] is not None:
        response = requests.get(people_dict['next'])
        people_dict = response.json()
        people_list += people_dict['results']
    return people_list


def convert_data(data):
    date = dt.now().strftime("%Y-%m-%d")
    time = dt.now().strftime("%H-%M-%S")
    columns = list(data[0].keys())
    table = (
        etl
        .fromdicts(data, header=columns[:9])
        .convert('homeworld', get_homeworld_name, pass_row=True)
        .addfield('date', date))
    filepath = f'star_wars/static/datasets/'
    filename = f'{date + "_" + time}.csv'

    etl.tocsv(table, filepath + filename)
    size = os.stat(filepath + filename).st_size / 1000
    extension = os.path.splitext(filename)[-1]
    filepath_abs = os.path.relpath(filepath + filename)
    DataSet.objects.create(filename=filename, date=dt.now(), size=f'{size}KB', extension=extension,
                           filepath=filepath_abs)


def get_homeworld_name(val, row):
    response = requests.get(val)
    planet_dict = response.json()
    planet = planet_dict["name"]
    return planet


def read_dataset(filepath):
    table = etl.fromcsv(filepath)
    header = etl.header(table)
    return table, header, header


def count_dataset(filepath, parameters):
    table = etl.fromcsv(filepath)
    table1 = etl.valuecounts(table, *parameters)
    table2 = etl.convert(table1, 'frequency', round_frequency, pass_row=True)
    header = etl.header(table2)
    buttons = etl.header(table)
    return table2, header, buttons


def round_frequency(val, row):
    return round(val, 3)
