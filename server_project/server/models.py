from django.db import models

class Document(models.Model):
    name = models.TextField()
    path = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.TextField()
    main_entity = models.TextField()
    entities = models.TextField()
    faculty = models.TextField()
    pj_id = models.TextField()
    program = models.TextField()
    pj_type = models.TextField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    chief = models.ForeignKey(ProjectChief, on_delete=models.CASCADE)


class Program(models.Model):
    name = models.TextField;
    chief = models.OneToOneField(ProgramChief, on_delete=models.CASCADE)


class ProjectChief(models.User):
    name = models.TextField()
    
class ProgramChief(models.User):
    name = models.TextField()
