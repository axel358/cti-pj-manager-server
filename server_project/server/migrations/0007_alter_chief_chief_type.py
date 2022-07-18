# Generated by Django 4.0.5 on 2022-07-18 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_groupdocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chief',
            name='chief_type',
            field=models.TextField(choices=[('project_program_both_chief', 'Jefe de Proyecto/ Programa / Ambos'), ('human_res', 'Recursos Humanos'), ('economy', 'Economia'), ('vicedec_inv_postgr', 'Vicedecano de Investigacion y Postgrado')], default='human_res', max_length=255),
        ),
    ]