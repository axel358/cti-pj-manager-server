# Generated by Django 4.0.5 on 2022-07-15 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0014_remove_project_faculty_remove_project_pj_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='organization',
            field=models.CharField(default='', max_length=500),
        ),
    ]
