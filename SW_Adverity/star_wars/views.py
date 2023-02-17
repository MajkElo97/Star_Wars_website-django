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
    if request.method == 'POST':
        global people_to_display
        people_to_display += 10
        return redirect(".")
    visible = True
    obj = get_object_or_404(DataSet, id=id_)
    dataset = read_dataset(obj.filepath)
    if people_to_display >= len(dataset[0]) - 1:
        visible = False
    context = {
        'dataset': dataset[0][1:people_to_display + 1],
        'header': dataset[1],
        'visible': visible,
    }
    return render(request, "dataset_detail.html", context)

