# Generated by Django 3.2.2 on 2021-07-26 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0005_element_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='description',
            field=models.TextField(default='No description available'),
        ),
    ]
