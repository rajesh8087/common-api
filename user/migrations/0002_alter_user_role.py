# Generated by Django 4.1.7 on 2023-02-24 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Super Admin', 'Super Admin'), ('Franchise Admin', 'Franchise Admin'), ('Admin', 'Admin'), ('Manager', 'Manager'), ('Assistant Manager', 'Assistant Manager'), ('Associate', 'Associate')], default='Super Admin', max_length=50),
        ),
    ]