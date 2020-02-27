# Generated by Django 2.2 on 2020-02-26 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20200226_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='contact',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='customer/'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='contact',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='manager',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='manager/'),
        ),
    ]
