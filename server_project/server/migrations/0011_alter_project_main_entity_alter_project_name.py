# Generated by Django 4.0.6 on 2022-07-29 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0010_projectdocument_dtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='main_entity',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
