# Generated by Django 4.1.7 on 2023-02-25 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_remove_company_documents'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='documents',
            field=models.FileField(blank=True, default='N/A', null=True, upload_to='media/'),
        ),
    ]
