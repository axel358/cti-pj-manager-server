# Generated by Django 4.0.5 on 2022-07-03 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_chief_remove_projectchief_user_ptr_program_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chief',
            options={'verbose_name': 'Chief'},
        ),
    ]