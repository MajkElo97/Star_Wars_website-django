# Generated by Django 4.1.7 on 2023-02-16 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('star_wars', '0002_alter_dataset_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
    ]
