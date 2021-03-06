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


class ProgramSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'name']


class ProgramSerializer(serializers.ModelSerializer):
    documents = ProgramDocumentSerializer(read_only=True, many=True)

    class Meta:
        model = Program
        fields = '__all__'

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


class ProjectSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class ProjectSerializer(serializers.ModelSerializer):
    documents = ProjectDocumentSerializer(read_only=True, many=True)
    document_groups = DocumentGroupSerializer(read_only=True, many=True)
    members = MembersSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = '__all__'
        # depth = 1

    def create(self, validated_data):
        chief = validated_data["chief"]
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
        user = self.context["request"].user
        if Chief.objects.exclude(pk=user.pk).filter(username=value).exists():
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
        if instance.chief_type != 'project_program_both_chief':
            group, created = Group.objects.get_or_create(name=instance.chief_type)
            instance.groups.clear()
            group.user_set.add(instance)

        return instance


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chief
        fields = '__all__'
