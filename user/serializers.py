from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, Permission
from school.models import School

MyUser = get_user_model()


class SchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['name']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class GroupListSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class MyUserListSerializer(serializers.ModelSerializer):
    schools = SchoolListSerializer()

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'is_active', 'is_admin', 'is_staff', 'schools', 'password']


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'is_active', 'is_admin', 'is_staff', 'password', 'groups',
                  'user_permissions', 'schools']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # def create(self, validated_data):
    #     if validated_data['email'] is '':
    #         user = MyUser.objects.create(
    #             username = validated_data['username']
    #         )
    #     else:
    #         user = MyUser.objects.create(
    #             username = validated_data['username'],
    #             email = validated_data['email']
    #         )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        schools = validated_data['schools']
        is_active = validated_data['is_active']
        is_admin = validated_data['is_admin']
        password = validated_data['password']
        user = MyUser(email=email,
                      username=username,
                      is_active=is_active,
                      is_admin=is_admin,
                      schools=schools
                      )
        groups = validated_data.get("groups")
        permissions = validated_data.get('user_permissions')
        try:
            for group in groups:
                user.groups.add(group)
        except:
            pass
        try:
            for permission in permissions:
                user.permissions.add(permission)
        except:
            pass
        user.set_password(password)
        user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if not attrs['password'] == attrs['confirm_password']:
            raise ValidationError('Passwords dont Match')
        return attrs
