# Generated by Django 2.2 on 2020-02-23 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.CharField(default='', max_length=10),
        ),
    ]
