# Generated by Django 3.0.1 on 2020-03-09 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_deaths'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmed',
            name='country_code',
            field=models.CharField(default='00', max_length=2),
        ),
        migrations.AddField(
            model_name='deaths',
            name='country_code',
            field=models.CharField(default='00', max_length=2),
        ),
    ]
