from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(Program)
admin.site.register(Chief)
admin.site.register(ProjectDocument)
admin.site.register(ProgramDocument)
admin.site.register(DocumentGroup)
admin.site.register(GroupDocument)
admin.site.register(Member)


