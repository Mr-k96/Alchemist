from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 댓글 작성자의 username 반환

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article')

class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 게시글 작성자의 username 반환

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'user')  # user 필드 추가

class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 게시글 작성자의 username 반환
    comments = CommentSerializer(many=True, read_only=True)  # 댓글 포함

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)
