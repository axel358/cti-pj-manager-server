from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
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


class ProgramDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramDocument
        fields = '__all__'


class GroupDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDocument
        fields = '__all__'


class DocumentGroupSerializer(serializers.ModelSerializer):
    documents = GroupDocumentSerializer(read_only=True, many=True)

    class Meta:
        model = DocumentGroup
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    documents = ProgramDocumentSerializer(read_only=True, many=True)

    class Meta:
        model = Program
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    documents = ProjectDocumentSerializer(read_only=True, many=True)
    document_groups = DocumentGroupSerializer(read_only=True, many=True)
    members = MembersSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'project_code', 'program', 'program_code', 'project_classification', 'pj_type',
            'main_entity', 'entities', 'start_date', 'end_date', 'financing', 'chief',
            'documents', 'document_groups', 'members')
        # depth = 1


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
        user = self.context["request"].user
        if Chief.objects.exclude(pk=25).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already in use."}
            )
        return value

    def validate_email(self, value):
        user = self.context["request"].user
        if Chief.objects.exclude(pk=user.pk).filter(email=value).exists():
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
        group, created = Group.objects.get_or_create(name=instance.chief_type)
        instance.groups.clear()
        group.user_set.add(instance)

        return instance


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chief
        fields = '__all__'
