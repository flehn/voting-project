# Generated by Django 3.2.2 on 2021-07-23 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_alter_element_voting'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='voting',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
