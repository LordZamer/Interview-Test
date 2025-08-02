# backend/app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    PageViewSet,
    PermissionViewSet,
    CommentViewSet,
    CommentHistoryViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pages', PageViewSet, basename='pages')
router.register(r'permissions', PermissionViewSet, basename='permissions')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'history', CommentHistoryViewSet, basename='history')

urlpatterns = [
    path('', include(router.urls)),
]
