# Generated by Django 3.2.2 on 2021-07-26 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0007_alter_element_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='link',
            field=models.CharField(blank=True, default='https://images.pexels.com/photos/2444429/pexels-photo-2444429.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260', max_length=300),
        ),
    ]
