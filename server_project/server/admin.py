from django.contrib import admin
from .models import Chief
from .models import Program
from .models import Document
from .models import Project

admin.site.register(Project)
admin.site.register(Program)
admin.site.register(Chief)
admin.site.register(Document)
