from rest_framework import viewsets, status, renderers
from rest_framework.permissions import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.http import FileResponse, HttpResponse
from wsgiref.util import FileWrapper
import mimetypes

from .serializers import *
from .permissions import *
import json


class MyTokenVerifyView(TokenVerifyView):
    serializer_class = MyTokenVerifySerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().filter()
    serializer_class = ProjectSerializer

    def retrieve(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project, context={'limited': False})

        if IsEconomyChief().has_permission(self.request, self):
            return Response(
                self.filter_documents(serializer.data, ['profile', 'rsjf', 'contract', 'dpac', 'cpie', 'cpr']))
        elif IsHumanResources().has_permission(self.request, self):
            return Response(self.filter_documents(serializer.data, ['bcpr', 'cpr']))

        return Response(serializer.data)

    def filter_documents(self, data, allowed_types):
        fd = []
        for document in data['documents']:
            if document['dtype'] in allowed_types:
                fd.append(document)

        data['documents'] = fd

        fdg = []

        for document_group in data['document_groups']:
            if document_group['dtype'] in allowed_types:
                fdg.append(document_group)

        data['document_groups'] = fdg

        return data

    def list(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        if IsProjectChief().has_permission(self.request, self):
            if request.headers["classification"] == 'all':
                serializer = ProjectSimpleSerializer(
                    queryset.filter(chief=request.user.id), many=True)
            elif request.headers["classification"] == 'pnap':
                serializer = ProjectSimpleSerializer(
                    queryset.filter(chief=request.user.id).filter(program=None), many=True)
            else:
                serializer = ProjectSimpleSerializer(
                    queryset.filter(chief=request.user.id).filter(pj_type=request.headers["classification"]), many=True)
        else:
            if request.headers["classification"] == 'all':
                serializer = ProjectSimpleSerializer(queryset, many=True)
            elif request.headers["classification"] == 'pnap':
                serializer = ProjectSimpleSerializer(queryset.filter(program=None), many=True)
            else:
                serializer = ProjectSimpleSerializer(queryset.filter(pj_type=request.headers["classification"]),
                                                     many=True)

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
            self.permission_classes = [
                IsAuthenticated & IsAdminUser | IsProjectChief | IsHumanResources | IsEconomyChief]
        else:
            self.permission_classes = [IsAuthenticated & IsAdminUser | IsProjectChief]
        return super(ProjectViewSet, self).get_permissions()


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def list(self, request, *args, **kwargs):
        queryset = Program.objects.all()
        serializer = ProgramSimpleSerializer(queryset, many=True)
        if IsAdminUser().has_permission(self.request, self):
            serializer = ProgramSimpleSerializer(queryset, many=True)
        else:
            serializer = ProgramSimpleSerializer(queryset.filter(chief=request.user.id), many=True)
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


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(methods=['get'], detail=True)
    def download(self, *args, **kwargs):
        instance = self.get_object()

        file_handle = instance.file.open()

        mimetype, _ = mimetypes.guess_type(instance.file.path)
        response = FileResponse(file_handle, content_type=mimetype)
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.file.name

        return response
        
    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        if document.file is not None:
            document.file.delete()
        self.perform_destroy(document)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectDocumentViewSet(DocumentViewSet):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer


class GroupDocumentViewSet(DocumentViewSet):
    queryset = GroupDocument.objects.all()
    serializer_class = GroupDocumentSerializer

    def destroy(self, request, *args, **kwargs):
        group_document = self.get_object()
        document_group = DocumentGroup.objects.get(id=group_document.group.id)
        if len(document_group.documents.values_list(flat=False)) == 1:
            self.perform_destroy(group_document)
            document_group.delete()
        else:
            self.perform_destroy(group_document)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentGroupViewSet(viewsets.ModelViewSet):
    queryset = DocumentGroup.objects.all()
    serializer_class = DocumentGroupSerializer

    def list(self, request, *args, **kwargs):
        queryset = DocumentGroup.objects.all()
        serializer = DocumentGroupSerializer(
            queryset.filter(dtype=request.headers["Name"]).filter(project=request.headers["Project"]), many=True)
        return Response(serializer.data)
