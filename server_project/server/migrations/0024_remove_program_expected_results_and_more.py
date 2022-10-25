# Generated by Django 4.1 on 2022-10-24 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0023_member_m_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='expected_results',
        ),
        migrations.RemoveField(
            model_name='program',
            name='experts_group',
        ),
        migrations.RemoveField(
            model_name='program',
            name='general_goals',
        ),
        migrations.RemoveField(
            model_name='program',
            name='indicators',
        ),
        migrations.RemoveField(
            model_name='program',
            name='infrastructure',
        ),
        migrations.RemoveField(
            model_name='program',
            name='main_results',
        ),
        migrations.RemoveField(
            model_name='program',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='program',
            name='reason',
        ),
        migrations.RemoveField(
            model_name='program',
            name='specific_goals',
        ),
        migrations.RemoveField(
            model_name='program',
            name='user_clients',
        ),
        migrations.AddField(
            model_name='chief',
            name='c_id',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='strategics_sectors',
            field=models.TextField(choices=[('tur', 'Turismo'), ('ind_biofarm', 'Industria boitecnológica y farmacéutica'), ('elec', 'Electroenergético'), ('pro_alim', 'Producción de alimentos'), ('constr', 'Construcciones'), ('tele_inf', 'Telecomunicaciones e Informática'), ('log_trans', 'Logística y transporte'), ('hidro_sanit', 'Redes hidráulicas y sanitarias'), ('agro_azucar', 'Agroindustria azucarera'), ('ind_ligera', 'Industria ligera'), ('ser_tecprof', 'Servicios técnicos profesionales')], default='tur'),
        ),
        migrations.AddField(
            model_name='project',
            name='strategics_sectors',
            field=models.TextField(choices=[('tur', 'Turismo'), ('ind_biofarm', 'Industria boitecnológica y farmacéutica'), ('elec', 'Electroenergético'), ('pro_alim', 'Producción de alimentos'), ('constr', 'Construcciones'), ('tele_inf', 'Telecomunicaciones e Informática'), ('log_trans', 'Logística y transporte'), ('hidro_sanit', 'Redes hidráulicas y sanitarias'), ('agro_azucar', 'Agroindustria azucarera'), ('ind_ligera', 'Industria ligera'), ('ser_tecprof', 'Servicios técnicos profesionales')], default='tur'),
        ),
        migrations.AlterField(
            model_name='member',
            name='m_type',
            field=models.TextField(choices=[('in', 'Interno'), ('out', 'Externo'), ('stdnt', 'Estudiante')], default='in', max_length=255),
        ),
    ]
