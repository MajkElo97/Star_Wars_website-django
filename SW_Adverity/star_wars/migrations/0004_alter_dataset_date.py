# Generated by Django 4.1.7 on 2023-02-16 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('star_wars', '0003_alter_dataset_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
