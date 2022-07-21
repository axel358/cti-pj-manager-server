from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import *


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        group, created = Group.objects.get_or_create(name='project_chiefs')
        is_have_only_one = Project.objects.exclude(id=project.id).filter(chief=project.chief.id).exists()
        if not is_have_only_one:
            group.user_set.remove(project.chief)

        return super(ProjectViewSet, self).destroy(request, *args, **kwargs)


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def destroy(self, request, *args, **kwargs):
        program = self.get_object()
        if program.chief is not None:
            group, created = Group.objects.get_or_create(name='program_chiefs')
            group.user_set.remove(program.chief)

        return super(ProgramViewSet, self).destroy(request, *args, **kwargs)


class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MembersSerializer


class ProjectDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer
