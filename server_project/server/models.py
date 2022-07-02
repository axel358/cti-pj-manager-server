from django.db import models
from django.contrib.auth.models import User


class Chief(User):
    name = models.TextField()
    is_program_chief = models.BooleanField()


class Program(models.Model):
    name = models.TextField(default='')
    chief = models.OneToOneField(Chief, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.TextField()
    main_entity = models.TextField()
    entities = models.TextField()
    faculty = models.TextField()
    pj_id = models.TextField()
    program = models.TextField()
    pj_type = models.TextField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    chief = models.ForeignKey(Chief, on_delete=models.CASCADE)


class Document(models.Model):
    name = models.TextField()
    path = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
