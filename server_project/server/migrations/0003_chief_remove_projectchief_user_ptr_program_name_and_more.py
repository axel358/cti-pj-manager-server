# Generated by Django 4.0.5 on 2022-07-02 18:04

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('server', '0002_alter_projectchief_options_delete_ttt'),
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
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='projectchief',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='program',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='program',
            name='chief',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='server.chief'),
        ),
        migrations.AlterField(
            model_name='project',
            name='chief',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.chief'),
        ),
        migrations.DeleteModel(
            name='ProgramChief',
        ),
        migrations.DeleteModel(
            name='ProjectChief',
        ),
    ]