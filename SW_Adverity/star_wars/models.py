from django.db import models
from django.urls import reverse


# Create your models here.
class DataSet(models.Model):
    filename = models.TextField()
    date = models.DateTimeField()
    size = models.CharField(max_length=120)
    extension = models.CharField(max_length=120)
    filepath = models.TextField()

    def get_absolute_url(self):
        return reverse("dataset-detail-view", kwargs={"id_": self.id})
