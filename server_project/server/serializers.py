from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenVerifySerializer, TokenObtainPairSerializer

from .models import *
from django.contrib.auth.models import Group, Permission


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class ProjectDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = '__all__'

    def validate(self, attrs):
        if ProjectDocument.objects.filter(project=attrs['project']).filter(name=attrs['name']).exists():
            raise serializers.ValidationError(
                {"exist": "This document already exists "}
            )
        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['d_name'] = instance.name if instance.dtype == 'other' else instance.get_dtype_display()
        return response


class ProgramDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramDocument
        fields = '__all__'


class GroupDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDocument
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['d_name'] = instance.group.name + '_' + str(
            instance.date) if instance.group.dtype == 'other' else instance.group.get_dtype_display() + '_' + str(instance.date)
        return response


class DocumentGroupSerializer(serializers.ModelSerializer):
    documents = GroupDocumentSerializer(read_only=True, many=True)

    class Meta:
        model = DocumentGroup
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['d_name'] = instance.name if instance.dtype == 'other' else instance.get_dtype_display()
        return response


class ProjectSimpleSerializer(serializers.ModelSerializer):
    chief = serializers.SerializerMethodField()
    project_classification = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'chief', 'end_date', 'project_classification']

    def get_chief(self, obj):
        return obj.chief.first_name + ' ' + obj.chief.last_name

    def get_project_classification(self, obj):
        return obj.get_project_classification_display()


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
        response['chief'] = instance.chief.first_name + ' ' + instance.chief.last_name
        response['type'] = instance.get_ptype_display()
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
        response['chief'] = instance.chief.first_name + ' ' + instance.chief.last_name
        response['type'] = instance.get_pj_type_display()
        response['classification'] = instance.get_project_classification_display()
        return response

    def create(self, validated_data):
        chief = validated_data['chief']
        group, created = Group.objects.get_or_create(name='project_chiefs')
        group.user_set.add(chief)
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.chief != validated_data['chief']:
            group, created = Group.objects.get_or_create(name='project_chiefs')
            is_have_more_projects = Project.objects.exclude(id=instance.id).filter(chief=instance.chief.id).exists()
            if not is_have_more_projects:
                group.user_set.remove(instance.chief)
            group.user_set.add(validated_data['chief'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


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
        )
        extra_kwargs = {
            "username": {"required": True},
            "password": {"required": True},
            "password2": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "chief_type": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = Chief.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            chief_type=validated_data["chief_type"],
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
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Chief
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."}
            )

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
        )
        extra_kwargs = {
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "chief_type": {"required": True},

        }

    def validate_username(self, value):
        if Chief.objects.exclude(id=self.instance.id).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already in use."}
            )
        return value

    def validate_email(self, value):
        if Chief.objects.exclude(id=self.instance.id).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )
        return value

    def update(self, instance, validated_data):
        # user = self.context["request"].user

        # if user.pk != instance.pk:
        #     raise serializers.ValidationError(
        #         {"authorize": "You dont have permission for this user."}
        #     )
        instance.username = validated_data["username"]
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        instance.chief_type = validated_data["chief_type"]

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


class MyTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
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
        data['groups'] = {self.user.groups.values_list('name', flat=True)}
        return data
