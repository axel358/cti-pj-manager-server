# Generated by Django 4.1 on 2022-11-27 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0031_remove_chief_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='chief',
            name='faculty',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
