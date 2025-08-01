from rest_framework import serializers
from .models import Page, PageComment, User, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'user')


class PageCommentSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = PageComment
        fields = ('id', 'comment', 'page')


class PageSerializer(serializers.ModelSerializer):
    page_id = serializers.UUIDField(read_only=True)
    Pcomment = PageCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ('page_id', 'name', 'Pcomment')
