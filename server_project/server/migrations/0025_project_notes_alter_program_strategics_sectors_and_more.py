# Generated by Django 4.1 on 2022-10-26 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0024_remove_program_expected_results_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='strategics_sectors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='strategics_sectors',
            field=models.TextField(blank=True, null=True),
        ),
    ]
