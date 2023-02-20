from django.shortcuts import render, redirect, get_object_or_404
from .functions import get_swapi, count_dataset, read_dataset
from .models import DataSet

rows_to_display = 10


# Home view with datasets
def home_view(request):
    global rows_to_display
    if request.method == 'POST':
        get_swapi()
        return redirect(".")
    rows_to_display = 10
    queryset = DataSet.objects.all().order_by('-id')
    context = {
        'object_list': queryset
    }
    return render(request, 'index.html', context)


# Dataset view with all characters
def dataset_detail_view(request, id_):
    global rows_to_display
    parameters = request.GET
    obj = get_object_or_404(DataSet, id=id_)

    if len(parameters) == 0:
        if request.method == 'POST':
            rows_to_display += 10
            return redirect(".")

        visible = True
        dataset = read_dataset(obj.filepath)
        if rows_to_display >= len(dataset[0]) - 1:
            visible = False

        context = {
            'dataset': dataset[0][1:rows_to_display + 1],
            'header': dataset[1],
            'buttons': dataset[2],
            'visible': visible,
        }
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

# Future improvments:
# - add search functionality
# - when fetching new dataset compare it with previous one so we avoid duplicates
# - improve the design of the page
# - Thing about efficiency: I already implement the function to lower the amount of requests for getting the planet name.
# - Time the app needs to fetch new data from SWAPI depends mostly on SWAPI server. The fastest time I get was about 5s
