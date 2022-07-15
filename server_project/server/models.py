import os

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Chief(User):
    name = models.TextField()
    is_program_chief = models.BooleanField()

    class Meta:
        verbose_name = 'Chief'


class Program(models.Model):
    PROGRAM_TYPES = [('nac', 'Nacional'),
                     ('sec', 'Sectorial'),
                     ('ter', 'Territorial')]
    name = models.CharField(max_length=512)
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
    start_date = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)
    pj_amount = models.IntegerField(null=True, blank=True)
    money = models.IntegerField(null=True, blank=True)
    user_clients = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProgramDocument(models.Model):

    def get_upload_folder(self, filename):
        return os.path.join(self.program.name, filename)

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
        ('i_bas', 'De Investigación Básica'),
        ('i_d', 'Aplicada y de Desarrollo'),
        ('inn', 'Innovación')
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
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
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


class Document(models.Model):

    def get_upload_folder(self, filename):
        return os.path.join(self.project.name, filename)

    name = models.TextField()
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='documents')
    file = models.FileField(upload_to=get_upload_folder, null=True)

    def __str__(self):
        return self.name
