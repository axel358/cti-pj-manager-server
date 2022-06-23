from django.contrib import admin
from .models import ProgramChief
from .models import Program
from .models import Document
from .models import Project
from .models import ProjectChief

admin.site.register(Project)
admin.site.register(Program)
admin.site.register(ProgramChief)
admin.site.register(ProjectChief)
admin.site.register(Document)


