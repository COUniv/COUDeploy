# Generated by Django 2.2.28 on 2022-11-15 03:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0016_auto_20220816_0744'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=list, size=None), blank=True, default=list, size=None)),
                ('update_expire_time', models.DateTimeField(null=True)),
            ],
        ),
    ]