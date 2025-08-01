from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Page, PageComment, PagePermission
from .serializers import CommentSerializer, PageSerializer, PageCommentSerializer
from rest_framework.exceptions import PermissionDenied

class PageAccessPermissionMixin:
    permission_type = None  # override in subclasses: 'view', 'edit', etc.

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return super().get_queryset()

        page_ids = PagePermission.objects.filter(
            user=user,
            access_type=self.permission_type
        ).values_list('page_id', flat=True)

        if hasattr(super(), 'get_queryset'):
            return super().get_queryset().filter(page_id__in=page_ids)
        return super().get_queryset()

    def has_page_permission(self, page):
        if self.request.user.is_super_admin:
            return True
        return PagePermission.objects.filter(
            user=self.request.user,
            page=page,
            access_type=self.permission_type
        ).exists()

class CommentViewSet(PageAccessPermissionMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    permission_type = 'view'

    def perform_update(self, serializer):
        comment = self.get_object()
        if not self.has_page_permission(comment.pagecomment.page):
            raise PermissionDenied("No edit permission for this page.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.has_page_permission(instance.pagecomment.page):
            raise PermissionDenied("No delete permission for this page.")
        instance.delete()

class PageViewSet(PageAccessPermissionMixin, viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated]
    permission_type = 'view'

class PageCommentViewSet(PageAccessPermissionMixin, viewsets.ModelViewSet):
    queryset = PageComment.objects.all()
    serializer_class = PageCommentSerializer
    permission_classes = [IsAuthenticated]
    permission_type = 'view'

    def perform_create(self, serializer):
        if not self.has_page_permission(serializer.validated_data['page']):
            raise PermissionDenied("No create permission for this page.")
        serializer.save()

    def perform_update(self, serializer):
        if not self.has_page_permission(serializer.instance.page):
            raise PermissionDenied("No edit permission for this page.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.has_page_permission(instance.page):
            raise PermissionDenied("No delete permission for this page.")
        instance.delete()
