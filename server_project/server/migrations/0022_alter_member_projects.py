# Generated by Django 4.0.6 on 2022-10-21 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0021_alter_member_c_id_alter_member_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='members', to='server.project'),
        ),
    ]
