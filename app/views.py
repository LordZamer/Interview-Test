from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Page, Permission, Comment, CommentHistory
from .serializers import (
    UserSerializer, PageSerializer, PermissionSerializer,
    CommentSerializer, CommentHistorySerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save()


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Permission.objects.all()
        return Permission.objects.filter(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Comment.objects.all()
        user_permissions = Permission.objects.filter(user=self.request.user, permission_type='view')
        return Comment.objects.filter(page__in=[p.page for p in user_permissions])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        CommentHistory.objects.create(
            comment=instance,
            modified_by=self.request.user,
            original_content=self.request.data.get('content', '')
        )


class CommentHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommentHistory.objects.all()
    serializer_class = CommentHistorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CommentHistory.objects.all()
        return CommentHistory.objects.none()
