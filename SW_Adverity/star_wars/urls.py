from django.urls import path
from .views import home_view, dataset_detail_view

urlpatterns = [
    path('', home_view, name='home-view'),
    path('<int:id_>/', dataset_detail_view, name='dataset-detail-view'),
]
