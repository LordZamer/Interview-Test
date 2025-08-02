from rest_framework import serializers
from .models import User, Page, Permission, Comment, CommentHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'is_staff', 'date_joined']


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name']


class PermissionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())

    class Meta:
        model = Permission
        fields = ['id', 'user', 'page', 'permission_type']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    page = PageSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'page', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CommentHistorySerializer(serializers.ModelSerializer):
    modified_by = UserSerializer(read_only=True)

    class Meta:
        model = CommentHistory
        fields = ['id', 'comment', 'modified_by', 'original_content', 'modified_at']
        read_only_fields = ['id', 'modified_at']
