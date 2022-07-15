import os
from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return self.name


class ProgramDocument(models.Model):

    def get_upload_folder(self, filename):
        return os.path.join(self.program.name, filename)

    name = models.TextField()
    file = models.FileField(upload_to=get_upload_folder, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='documents', null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    PROJECTS_TYPES = [('pap', 'Proyectos Asociados a Programas'),
                      ('pnap', 'Proyectos No Asociados a Programas')]
    name = models.TextField()
    main_entity = models.TextField()
    entities = models.TextField()
    faculty = models.TextField()
    pj_id = models.TextField()
    pj_type = models.TextField(max_length=255,
                               choices=PROJECTS_TYPES,
                               default='pap')
    program = models.ForeignKey(Program,
                                on_delete=models.CASCADE,
                                related_name='projects',
                                null=True,
                                blank=True)
    chief = models.ForeignKey(Chief,
                              on_delete=models.CASCADE,
                              related_name='projects')

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.TextField()
    email = models.EmailField(max_length=254)
    c_id = models.TextField(max_length=11)
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
