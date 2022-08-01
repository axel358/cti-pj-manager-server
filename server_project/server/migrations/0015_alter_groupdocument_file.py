# Generated by Django 4.0.6 on 2022-08-01 13:08

from django.db import migrations, models
import server.models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0014_alter_documentgroup_name_alter_projectdocument_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupdocument',
            name='file',
            field=models.FileField(blank=True, max_length=512, null=True, upload_to=server.models.GroupDocument.get_upload_folder),
        ),
    ]