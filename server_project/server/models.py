import os
from django.db import models
from django.contrib.auth.models import User


class Chief(User):
    name = models.TextField()
    is_program_chief = models.BooleanField()

    class Meta():
        verbose_name = 'Chief'


class Program(models.Model):
    name = models.TextField(default='')
    chief = models.OneToOneField(Chief, on_delete=models.CASCADE, related_name='program')

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.TextField()
    main_entity = models.TextField()
    entities = models.TextField()
    faculty = models.TextField()
    pj_id = models.TextField()
    program = models.TextField()
    pj_type = models.TextField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='projects')
    chief = models.ForeignKey(Chief, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name


class Document(models.Model):

    def get_upload_folder(self, filename):
        return os.path.join(self.project.name, filename)

    name = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to=get_upload_folder, null=True)

    def __str__(self):
        return self.name



