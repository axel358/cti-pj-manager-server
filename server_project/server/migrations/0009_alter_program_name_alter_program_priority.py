# Generated by Django 4.0.6 on 2022-07-15 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_programdocument_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='program',
            name='priority',
            field=models.TextField(null=True),
        ),
    ]
