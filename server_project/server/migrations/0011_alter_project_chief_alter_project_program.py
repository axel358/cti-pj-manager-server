# Generated by Django 4.0.5 on 2022-07-07 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0010_alter_project_pj_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='chief',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pro_chief', to='server.chief'),
        ),
        migrations.AlterField(
            model_name='project',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program', to='server.program'),
        ),
    ]
