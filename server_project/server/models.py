import datetime
import os

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Chief(User):
    USERS_ROLES = [
        ('project_program_both_chief', 'Jefe de Proyecto/ Programa / Ambos'),
        ('human_resources', 'Recursos Humanos'),
        ('economy', 'Economia'),
        ('vicedec_inv_postgr', 'Vicedecano de Investigacion y Postgrado')

    ]
    chief_type = models.TextField(max_length=255, choices=USERS_ROLES, default='human_res')

    class Meta:
        verbose_name = 'Chief'


class Program(models.Model):
    PROGRAM_TYPES = [('nac', 'Nacional'),
                     ('sec', 'Sectorial'),
                     ('ter', 'Territorial')]
    name = models.CharField(max_length=512)
    program_code = models.CharField(max_length=10, default="0")
    chief = models.OneToOneField(Chief,
                                 on_delete=models.CASCADE,
                                 related_name='program',
                                 null=True, blank=True)
    priority = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    ptype = models.TextField(choices=PROGRAM_TYPES, default='nac')
    general_goals = models.TextField(null=True, blank=True)
    specific_goals = models.TextField(null=True, blank=True)
    main_results = models.TextField(null=True, blank=True)
    indicators = models.TextField(null=True, blank=True)
    expected_results = models.TextField(null=True, blank=True)
    entities = models.TextField(null=True, blank=True)
    infrastructure = models.TextField(null=True, blank=True)
    main_entity = models.TextField(null=True, blank=True)
    secretary = models.TextField(null=True, blank=True)
    experts_group = models.TextField(null=True, blank=True)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    pj_amount = models.IntegerField(null=True, blank=True)
    money = models.BigIntegerField(null=True, blank=True)
    user_clients = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Program, self).save(*args, **kwargs)

    def clean_fields(self, exclude=None):
        if self.end_date < self.start_date:
            raise ValidationError('The start date must be less than the end date.')

    def __str__(self):
        return self.name


class ProgramDocument(models.Model):

    def get_upload_folder(self, filename):
        return os.path.join('Programas', self.program.name, filename)

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_upload_folder, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='documents', null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    PROJECTS_TYPES = [
        ('papn', 'Proyectos Asociados a Programas Nacional'),
        ('paps', 'Proyectos Asociados a Programas Sectorial'),
        ('papt', 'Proyectos Asociados a Programas Territorial'),
        ('pnap_di', 'Proyectos No Asociados a Programas Demanda Interna'),
        ('pnap_de', 'Proyectos No Asociados a Programas Demanda Externa')

    ]
    PROJECTS_CLASS_OPTIONS = [
        ('i_bas', 'De Investigaci??n B??sica'),
        ('i_d', 'Aplicada y de Desarrollo'),
        ('inn', 'Innovaci??n')
    ]
    name = models.TextField()
    project_code = models.CharField(max_length=10, default="0")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    program_code = models.CharField(max_length=10, default="0")
    project_classification = models.TextField(max_length=255, choices=PROJECTS_CLASS_OPTIONS, default='i_bas')
    pj_type = models.TextField(max_length=255, choices=PROJECTS_TYPES, default='papt')
    main_entity = models.TextField()
    entities = models.TextField()
    chief = models.ForeignKey(Chief, on_delete=models.CASCADE, related_name='projects')
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    financing = models.PositiveBigIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Project, self).save(*args, **kwargs)

    def clean_fields(self, exclude=None):
        if self.end_date < self.start_date:
            raise ValidationError('The start date must be less than the end date.')

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.TextField()
    email = models.EmailField(max_length=254)
    c_id = models.TextField(max_length=11)
    organization = models.CharField(max_length=500, default='')
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='members')

    def __str__(self):
        return self.name


class ProjectDocument(models.Model):

    def get_upload_folder(self, filename):
        program = self.project.program

        if program is not None:
            return os.path.join('Programas', program.name, 'Projectos', self.project.name, filename)
        else:
            return os.path.join('Projectos', self.project.name, filename)

    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='documents')
    file = models.FileField(upload_to=get_upload_folder, null=True, blank=True)
    DOCUMENT_TYPES = [('other', 'Otro'),
                     ('profile', 'Perfil'),
                     ('contract', 'Contract'),
                     ('rsjf', 'Resoluci??n de nombramiento del jefe de proyecto'),
                     ('cidef', 'Compatibilizaci??n con los intereses de la Defensa'),
                     ('roap', 'Resoluci??n oficial de aprobaci??n del proyecto'),
                     ('dapcca', 'Dictamen de aprobaci??n del proyecto por el CCA'),
                     ('dpddp', 'Documentos de planificaci??n del dise??o y desarrollo del producto'),
                     ('dpac', 'Desglose del presupuesto del a??o en curso'),
                     ('mca', 'Anexo 15 Modelo de certificaci??n de actividades'),
                     ('isp', 'Anexo 13 Informe semestral del proyecto'),
                     ('ict', 'Informe cient??fico t??cnico'),
                     ('dapiscca', 'Dictamen de aprobaci??n del informe semestral por el CCA'),
                     ('dgeri', 'Dictamen del Grupo de Expertos sobre los resultados y el Informe de la Etapa'),
                     ('mnig', 'Anexo 16 Modelo de Notificaci??n de Ingresos/Gastos'),
                     ('bcpr', 'Base de c??lculo para el pago por remuneraci??n'),
                     ('acpp', 'Acta de conformidad de los participantes del proyecto'),
                     ('cpr', 'Certificaci??n para el pago de la remuneraci??n'),
                     ('cpie', 'Anexo 8. Certifico para el pago de los investigadores externos'),
                     ('csbie', 'Certifico del salario b??sico de los investigadores externos'),
                     ('fciie', 'Fotos escaneadas del carn?? de identidad de los investigadores')]
    dtype = models.CharField(max_length=512, choices=DOCUMENT_TYPES, default='other')

    def __str__(self):
        return self.name


class DocumentGroup(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='document_groups')

    def __str__(self):
        return self.name


class GroupDocument(models.Model):

    def get_upload_folder(self, filename):
        program = self.group.project.program

        if program is not None:
            return os.path.join('Programas', program.name, 'Projectos', self.group.project.name, self.group.name,
                                filename)
        else:
            return os.path.join('Projectos', self.group.project.name, self.group.name, filename)

    name = models.CharField(max_length=255)
    group = models.ForeignKey(DocumentGroup,
                              on_delete=models.CASCADE,
                              related_name='documents')

    file = models.FileField(upload_to=get_upload_folder, null=True, blank=True)

    def __str__(self):
        return self.name
