from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
]

router = DefaultRouter()
router.register('comments', views.CommentViewSet)
router.register('pages', views.PageViewSet)
router.register('pageComents', views.PageCommentViewSet)
urlpatterns += router.urls