# Generated by Django 3.2.4 on 2021-07-13 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='number_of_votes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
