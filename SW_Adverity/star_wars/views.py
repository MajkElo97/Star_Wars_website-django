from django.shortcuts import render, redirect, get_object_or_404
from .functions import *

people_to_display = 10


# Create your views here.
def home_view(request):
    global people_to_display
    people_to_display = 10
    queryset = DataSet.objects.all().order_by('-id')
    context = {
        'object_list': queryset
    }
    return render(request, 'index.html', context)


def fetch_data_view(request):
    global people_to_display
    people_to_display = 10
    people = get_swapi()
    convert_data(people)
    return redirect(home_view)


def dataset_detail_view(request, id_):
    parameters = request.GET

    obj = get_object_or_404(DataSet, id=id_)
    if len(parameters) == 0:
        # print(request.GET)
        if request.method == 'POST':
            global people_to_display
            people_to_display += 10
            return redirect(".")
        visible = True
        dataset = read_dataset(obj.filepath)
        if people_to_display >= len(dataset[0]) - 1:
            visible = False
        context = {
            'dataset': dataset[0][1:people_to_display + 1],
            'header': dataset[1],
            'buttons': dataset[2],
            'visible': visible,
        }
        return render(request, "dataset_detail.html", context)
    else:
        count_parameters = list(parameters.dict().keys())
        dataset_counted = count_dataset(obj.filepath, count_parameters)
        context = {
            'dataset': dataset_counted[0][1:],
            'header': dataset_counted[1],
            'buttons': dataset_counted[2],
            'visible': False,
        }
        return render(request, "dataset_detail.html", context)
