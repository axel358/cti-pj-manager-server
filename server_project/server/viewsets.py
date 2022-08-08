from rest_framework import viewsets, status
from rest_framework.permissions import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import *
from .permissions import *
import json


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().filter()
    serializer_class = ProjectSerializer

    def retrieve(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project, context={'limited': False})

        if IsEconomyChief().has_permission(self.request, self):
            return Response(self.filter_documents(serializer.data, ['profile', 'rsjf', 'contract', 'dpac', 'cpie', 'cpr']))
        elif IsHumanResources().has_permission(self.request, self):
            return Response(self.filter_documents(serializer.data, ['bcpr', 'cpr']))

        return Response(serializer.data)

    def filter_documents(self, data, allowed_types):
        documents = data['documents']
        index = 0
        for document in documents:
            if document['dtype'] not in allowed_types:
                documents.pop(index)
            index += 1

        document_groups = data['document_groups']
        index = 0
        for document_group in document_groups:
            if document_group['dtype'] not in allowed_types:
                document_groups.pop(index)
            index += 1

        return data


    def list(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        if IsProjectChief().has_permission(self.request, self):
            serializer = ProjectSimpleSerializer(queryset.filter(chief=request.user.id), many=True)
        else:
            serializer = ProjectSimpleSerializer(queryset, many=True)
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

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated & IsAdminUser | IsProjectChief | IsHumanResources | IsEconomyChief]
        else:
            self.permission_classes = [IsAuthenticated, IsAdminUser, IsProjectChief]
        return super(ProjectViewSet, self).get_permissions()


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def list(self, request, *args, **kwargs):
        serializer = ProgramSimpleSerializer(self.queryset, many=True)
        if IsAdminUser().has_permission(self.request, self):
            serializer = ProgramSimpleSerializer(self.queryset, many=True)
        else:
            serializer = ProgramSimpleSerializer(self.queryset.filter(chief=request.user.id), many=True)
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
            self.permission_classes = [IsAuthenticated & IsAdminUser | IsProgramChief]
        else:
            self.permission_classes = [IsAuthenticated, IsAdminUser, ]
        return super(ProgramViewSet, self).get_permissions()


class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MembersSerializer


class ProjectDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer
