# Generated by Django 4.0.6 on 2022-07-30 14:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_remove_groupdocument_name_documentgroup_dtype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupdocument',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
