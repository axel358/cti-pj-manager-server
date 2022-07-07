# Generated by Django 4.0.5 on 2022-07-04 17:36

from django.db import migrations, models
import server.models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_alter_document_file_alter_document_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(null=True, upload_to=server.models.Document.get_upload_folder),
        ),
    ]