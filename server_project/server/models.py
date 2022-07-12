import os
from django.db import models
from django.contrib.auth.models import User


class Chief(User):
    name = models.TextField()
    is_program_chief = models.BooleanField()

    class Meta:
        verbose_name = 'Chief'


class Program(models.Model):
    name = models.TextField(default='')
    chief = models.OneToOneField(Chief, on_delete=models.CASCADE, related_name='program')

    def __str__(self):
        return self.name


class Project(models.Model):
    PROJECTS_TYPES = [
        ('pap', 'Proyectos Asociados a Programas'),
        ('pnap', 'Proyectos No Asociados a Programas')
    ]
    name = models.TextField()
    main_entity = models.TextField()
    entities = models.TextField()
    faculty = models.TextField()
    pj_id = models.TextField()
    pj_type = models.TextField(max_length=255, choices=PROJECTS_TYPES, default='pap')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='projects')
    chief = models.ForeignKey(Chief, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name


class Member(models.Model):
    full_name = models.TextField()
    email = models.EmailField(max_length=254)
    c_id = models.TextField(max_length=11)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return self.full_name


class Document(models.Model):

    def get_upload_folder(self, filename):
        return os.path.join(self.project.name, filename)

    name = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to=get_upload_folder, null=True)

    def __str__(self):
        return self.name
