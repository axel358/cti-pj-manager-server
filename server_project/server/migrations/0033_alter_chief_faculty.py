# Generated by Django 4.1 on 2022-11-28 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0032_chief_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chief',
            name='faculty',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
    ]
