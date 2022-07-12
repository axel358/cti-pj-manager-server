# Generated by Django 4.0.6 on 2022-07-12 17:57

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import server.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chief',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.TextField()),
                ('is_program_chief', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Chief',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('chief', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='program', to='server.chief')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('main_entity', models.TextField()),
                ('entities', models.TextField()),
                ('faculty', models.TextField()),
                ('pj_id', models.TextField()),
                ('pj_type', models.TextField(choices=[('pap', 'Proyectos Asociados a Programas'), ('pnap', 'Proyectos No Asociados a Programas')], default='pap', max_length=255)),
                ('chief', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='server.chief')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='server.program')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('c_id', models.TextField(max_length=11)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='server.project')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('file', models.FileField(null=True, upload_to=server.models.Document.get_upload_folder)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='server.project')),
            ],
        ),
    ]
