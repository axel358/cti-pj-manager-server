from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenVerifySerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from .models import *
from django.contrib.auth.models import Group, Permission


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def validate(self, attrs):
        if self.instance is not None:
            if Member.objects.exclude(id=self.instance.id).filter(c_id=attrs['c_id']).exists():
                raise serializers.ValidationError(
                    {"exist": "This member already exists "}
                )
            return attrs
        else:
            if Member.objects.filter(c_id=attrs['c_id']).exists():
                raise serializers.ValidationError(
                    {"exist": "This member already exists "}
                )
            return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type'] = instance.get_m_type_display()
        return response


class ProjectDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = '__all__'

    def validate(self, attrs):
        if ProjectDocument.objects.filter(project=attrs['project']).filter(dtype=attrs['dtype']).exists():
            raise serializers.ValidationError(
                {"exist": "This document already exists "}
            )
        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['file'] = instance.file.name
        response['path'] = 'projectdocuments/'
        response['d_name'] = instance.name if instance.dtype == 'other' else instance.get_dtype_display()
        return response


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['file'] = instance.file.name
        response['path'] = 'documents/'
        return response


class ProgramDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramDocument
        fields = '__all__'

    def validate(self, attrs):
        if ProgramDocument.objects.filter(program=attrs['program']).filter(dtype=attrs['dtype']).exists():
            raise serializers.ValidationError(
                {"exist": "This document already exists "}
            )
        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['file'] = instance.file.name
        response['path'] = 'programdocuments/'
        response['d_name'] = instance.name if instance.dtype == 'other' else instance.get_dtype_display()
        return response


class GroupDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDocument
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['path'] = 'groupdocuments/'
        response['d_name'] = instance.group.name + '_' + str(
            instance.date) if instance.group.dtype == 'other' else instance.group.get_dtype_display() + '_' + str(
            instance.date)
        return response


class DocumentGroupSerializer(serializers.ModelSerializer):
    documents = GroupDocumentSerializer(read_only=True, many=True)

    class Meta:
        model = DocumentGroup
        fields = '__all__'

    def create(self, validated_data):
        group = DocumentGroup.objects.create(
            name=validated_data["name"],
            project=validated_data["project"],
            dtype=validated_data["dtype"],
        )
        group.save()

        return group

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['d_name'] = instance.name if instance.dtype == 'other' else instance.get_dtype_display()
        return response


class ProgramGroupDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramGroupDocument
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['path'] = 'programgroupdocuments/'
        response['d_name'] = instance.group.name + '_' + str(
            instance.date) if instance.group.dtype == 'other' else instance.group.get_dtype_display() + '_' + str(
            instance.date)
        return response


class ProgramDocumentGroupSerializer(serializers.ModelSerializer):
    documents = ProgramGroupDocumentSerializer(read_only=True, many=True)

    class Meta:
        model = ProgramDocumentGroup
        fields = '__all__'

    def create(self, validated_data):
        group = ProgramDocumentGroup.objects.create(
            name=validated_data["name"],
            program=validated_data["program"],
            dtype=validated_data["dtype"],
        )
        group.save()

        return group

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['d_name'] = instance.name if instance.dtype == 'other' else instance.get_dtype_display()
        return response


class ProjectSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'end_date', 'pj_type', 'strategics_sectors', 'notes', 'status', 'main_entity',
                  'program']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['chief'] = instance.chief.first_name + ' ' + instance.chief.last_name
        response['project_classification'] = instance.get_pj_type_display()
        response['financing'] = instance.financing
        response['chief_id'] = instance.chief.id
        return response


class ProgramSimpleSerializer(serializers.ModelSerializer):
    projects_details = ProjectSimpleSerializer(source='projects', read_only=True, many=True)

    class Meta:
        model = Program
        fields = ['id', 'name', 'ptype', 'chief', 'end_date', 'projects_details']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['chief'] = instance.chief.first_name + ' ' + instance.chief.last_name
        response['classification'] = instance.get_ptype_display()
        return response


class ProgramSerializer(serializers.ModelSerializer):
    documents = ProgramDocumentSerializer(read_only=True, many=True)
    document_groups = ProgramDocumentGroupSerializer(read_only=True, many=True)

    class Meta:
        model = Program
        fields = '__all__'

    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError(
                {"start_date": "The start date must be less than the end date."}
            )

        return attrs

    def create(self, validated_data):
        chief = validated_data["chief"]
        if chief is not None:
            group, created = Group.objects.get_or_create(name='program_chiefs')
            group.user_set.add(chief)

        return Program.objects.create(**validated_data)

    def update(self, instance, validated_data):

        if instance.chief != validated_data['chief']:
            group, created = Group.objects.get_or_create(name='program_chiefs')
            group.user_set.remove(instance.chief)
            group.user_set.add(validated_data['chief'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['chief_name'] = instance.chief.first_name + ' ' + instance.chief.last_name
        response['chief_email'] = instance.chief.email
        response['type'] = instance.get_ptype_display()
        response['sectors'] = []
        if len(instance.strategics_sectors) != 0:
            for i in instance.strategics_sectors.split(','):
                response['sectors'].append({"id": i, "value": i})
        response['pj_amount'] = len(Project.objects.filter(program=instance.id))
        return response


class ProjectSerializer(serializers.ModelSerializer):
    documents = ProjectDocumentSerializer(read_only=True, many=True)
    document_groups = DocumentGroupSerializer(read_only=True, many=True)
    members = MembersSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = '__all__'

    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError(
                {"start_date": "The start date must be less than the end date."}
            )

        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['chief_name'] = instance.chief.first_name + ' ' + instance.chief.last_name
        response['chief_email'] = instance.chief.email
        response['type'] = instance.get_pj_type_display()
        response['sectors'] = []
        if len(instance.strategics_sectors) != 0:
            for i in instance.strategics_sectors.split(','):
                response['sectors'].append({"id": i, "value": i})
        if instance.program is not None:
            response['program_name'] = instance.program.name
        response['classification'] = instance.get_project_classification_display()
        return response

    def create(self, validated_data):
        validated_data.pop('members')
        chief = validated_data['chief']
        group, created = Group.objects.get_or_create(name='project_chiefs')
        group.user_set.add(chief)
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.members.clear()
        if instance.notes != validated_data['notes'] and len(validated_data['notes']):
            validated_data['status'] = 1
        elif len(validated_data['notes']):
            validated_data['status'] = 0
        if instance.chief != validated_data['chief']:
            group, created = Group.objects.get_or_create(name='project_chiefs')
            is_have_more_projects = Project.objects.exclude(id=instance.id).filter(chief=instance.chief.id).exists()
            if not is_have_more_projects:
                group.user_set.remove(instance.chief)
            group.user_set.add(validated_data['chief'])
        for v in validated_data['members']:
            memb = Member.objects.get(id=v.get('id'))
            instance.members.add(memb)

        for attr, value in validated_data.items():
            if attr == 'members':
                continue
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        internal_value = super(ProjectSerializer, self).to_internal_value(data)
        members_raw_value = data.get('members')
        internal_value.update({
            'members': members_raw_value
        })
        return internal_value


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=Chief.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    chief_type = serializers.ChoiceField(required=True, choices=Chief.USERS_ROLES)
    first_name = serializers.CharField(required=True, max_length=70)
    last_name = serializers.CharField(required=True, max_length=70)

    class Meta:
        model = Chief
        fields = (
            "username",
            "password",
            "password2",
            "first_name",
            "last_name",
            "email",
            "chief_type",
            "c_id",
            "faculty",
        )
        extra_kwargs = {
            "username": {"required": True},
            "password": {"required": True},
            "password2": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "chief_type": {"required": True},
            "c_id": {"required": False},
            "faculty": {"required": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_c_id(self, value):
        if value != "":
            if Chief.objects.filter(c_id=value).exists():
                raise serializers.ValidationError("This user already exists.")
        return value

    def create(self, validated_data):
        user = Chief.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            chief_type=validated_data["chief_type"],
            c_id=validated_data["c_id"],
            faculty=validated_data["faculty"],
        )
        user.set_password(validated_data["password"])
        if user.chief_type != 'project_program_both_chief':
            group, created = Group.objects.get_or_create(name=user.chief_type)
            group.user_set.add(user)
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Chief
        fields = ("password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Chief
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "chief_type",
            "c_id",
            "faculty",
        )
        extra_kwargs = {
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "chief_type": {"required": True},
            "c_id": {"required": False},
            "faculty": {"required": False},

        }

    def validate_username(self, value):
        if Chief.objects.exclude(id=self.instance.id).filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def validate_c_id(self, value):
        if value != "":
            if Chief.objects.exclude(id=self.instance.id).filter(c_id=value).exists():
                raise serializers.ValidationError("This user already exists.")
        return value

    def validate_email(self, value):
        if Chief.objects.exclude(id=self.instance.id).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):

        instance.username = validated_data["username"]
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        instance.chief_type = validated_data["chief_type"]
        instance.c_id = validated_data["c_id"]
        instance.faculty = validated_data["faculty"]

        instance.save()
        if instance.chief_type != 'project_program_both_chief':
            group, created = Group.objects.get_or_create(name=instance.chief_type)
            instance.groups.clear()
            group.user_set.add(instance)

        return instance


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chief
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name'] = instance.first_name + ' ' + instance.last_name
        response['type'] = instance.get_chief_type_display()
        return response


class MyTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        # user = OutstandingToken.objects.filter(token=self.initial_data['ref_token']).values_list('user_id', flat=True)
        # if not User.objects.filter(id=user[0]).exists():
        #
        #     raise serializers.ValidationError(
        #         {"email": "This user is not valid."}
        #     )
        data = super().validate(attrs)
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = {"username": self.user.username}
        data['email'] = {"email": self.user.email}
        data['user_id'] = str(self.user.id)
        if not self.user.is_superuser:
            data['faculty'] = str(Chief.objects.filter(username=self.user.username)[0].faculty)
        else:
            data['faculty'] = str('')
        if self.user.is_superuser:
            data['groups'] = ['admin']
        else:
            data['groups'] = self.user.groups.values_list('name', flat=True)
        return data
