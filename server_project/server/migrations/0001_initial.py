# Generated by Django 4.0.6 on 2022-07-16 15:26

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
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
                ('name', models.CharField(max_length=512)),
                ('program_code', models.CharField(default='0', max_length=10)),
                ('priority', models.TextField(blank=True, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('ptype', models.TextField(choices=[('nac', 'Nacional'), ('sec', 'Sectorial'), ('ter', 'Territorial')], default='nac')),
                ('general_goals', models.TextField(blank=True, null=True)),
                ('specific_goals', models.TextField(blank=True, null=True)),
                ('main_results', models.TextField(blank=True, null=True)),
                ('indicators', models.TextField(blank=True, null=True)),
                ('expected_results', models.TextField(blank=True, null=True)),
                ('entities', models.TextField(blank=True, null=True)),
                ('infrastructure', models.TextField(blank=True, null=True)),
                ('main_entity', models.TextField(blank=True, null=True)),
                ('secretary', models.TextField(blank=True, null=True)),
                ('experts_group', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('pj_amount', models.IntegerField(blank=True, null=True)),
                ('money', models.BigIntegerField(blank=True, null=True)),
                ('user_clients', models.TextField(blank=True, null=True)),
                ('chief', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='program', to='server.chief')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('project_code', models.CharField(default='0', max_length=10)),
                ('program_code', models.CharField(default='0', max_length=10)),
                ('project_classification', models.TextField(choices=[('i_bas', 'De Investigación Básica'), ('i_d', 'Aplicada y de Desarrollo'), ('inn', 'Innovación')], default='i_bas', max_length=255)),
                ('pj_type', models.TextField(choices=[('papn', 'Proyectos Asociados a Programas Nacional'), ('paps', 'Proyectos Asociados a Programas Sectorial'), ('papt', 'Proyectos Asociados a Programas Territorial'), ('pnap_di', 'Proyectos No Asociados a Programas Demanda Interna'), ('pnap_de', 'Proyectos No Asociados a Programas Demanda Externa')], default='papt', max_length=255)),
                ('main_entity', models.TextField()),
                ('entities', models.TextField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('financing', models.PositiveBigIntegerField(default=0)),
                ('chief', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='server.chief')),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='server.program')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('file', models.FileField(null=True, upload_to=server.models.ProjectDocument.get_upload_folder)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='server.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(blank=True, null=True, upload_to=server.models.ProgramDocument.get_upload_folder)),
                ('program', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='server.program')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('c_id', models.TextField(max_length=11)),
                ('organization', models.CharField(default='', max_length=500)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='server.project')),
            ],
        ),
    ]
