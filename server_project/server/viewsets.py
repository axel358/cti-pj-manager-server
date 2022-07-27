from rest_framework import viewsets, status
from rest_framework.permissions import *
from rest_framework.response import Response
from .serializers import *
from .permissions import *


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        serializer = ProjectSimpleSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        group, created = Group.objects.get_or_create(name='project_chiefs')
        is_have_more_projects = Project.objects.exclude(id=project.id).filter(chief=project.chief.id).exists()
        if not is_have_more_projects:
            group.user_set.remove(project.chief)

        # super(ProjectViewSet, self).destroy(request, *args, **kwargs)
        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def list(self, request, *args, **kwargs):
        serializer = ProgramSimpleSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        program = self.get_object()
        if program.chief is not None:
            group, created = Group.objects.get_or_create(name='program_chiefs')
            group.user_set.remove(program.chief)

        self.perform_destroy(program)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated, IsAdminUser | IsProgramChief]
        else:
            self.permission_classes = [IsAuthenticated, IsAdminUser, ]
        return super(ProgramViewSet, self).get_permissions()


class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MembersSerializer


class ProjectDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer
