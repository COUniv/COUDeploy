# Generated by Django 2.2.28 on 2022-11-28 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_manageduserlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manageduserlist',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]