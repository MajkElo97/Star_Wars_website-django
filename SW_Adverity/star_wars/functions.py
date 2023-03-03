import requests
from datetime import datetime as dt
import petl as etl
from .models import DataSet
import os

planet_dict = {}


# Function to get data from API
def get_swapi():
    global planet_dict
    planet_dict = {}
    response = requests.get('https://swapi.dev/api/people/')
    people_dict = response.json()
    people_list = people_dict['results']

    while people_dict['next'] is not None:
        response = requests.get(people_dict['next'])
        people_dict = response.json()
        people_list += people_dict['results']
    convert_data(people_list)


# Function to convert data from request into csv file and add record to DB
def convert_data(data):
    date = dt.now().strftime("%Y-%m-%d")
    time = dt.now().strftime("%H-%M-%S")
    columns = list(data[0].keys())
    table = (
        etl
        .fromdicts(data, header=columns[:9])
        .convert('homeworld', get_homeworld_name)
        .addfield('date', date))
    filepath = f'star_wars/static/datasets/'
    filename = f'{date + "_" + time}.csv'
    etl.tocsv(table, filepath + filename)
    size = os.stat(filepath + filename).st_size / 1000
    extension = os.path.splitext(filename)[-1]
    filepath_rel = os.path.relpath(filepath + filename)
    DataSet.objects.create(filename=filename, date=dt.now(), size=f'{size}KB', extension=extension,
                           filepath=filepath_rel)


# Function to convert API endpoint to planet name in column 'homeworld'
def get_homeworld_name(val):
    global planet_dict
    if val not in planet_dict.keys():
        response = requests.get(val)
        planet_json = response.json()
        planet = planet_json["name"]
        planet_dict[val] = planet
    else:
        planet = planet_dict[val]
    return planet


# Function for reading chosen dataset
def read_dataset(filepath):
    table = etl.fromcsv(filepath)
    header = etl.header(table)
    return table, header, header


# Function for count functionality
def count_dataset(filepath, parameters):
    table = etl.fromcsv(filepath)
    table1 = etl.valuecounts(table, *parameters)
    table2 = etl.convert(table1, 'frequency', round_frequency)
    header = etl.header(table2)
    buttons = etl.header(table)
    return table2, header, buttons


# Function for rounding frequency column
def round_frequency(val):
    return round(val, 3)


# Class for row displaying configuration
class Rows:
    def __init__(self):
        self.rows = 10

    def add_row(self):
        self.rows += 10
