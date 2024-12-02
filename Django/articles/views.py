from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import (
    ArticleListSerializer,
    ArticleSerializer,
    CommentSerializer
)
from .models import Article, Comment

class ArticlePagination(PageNumberPagination):
    page_size = 5  # 페이지당 게시글 수
    page_size_query_param = 'page_size'  # 쿼리 파라미터로 페이지 크기를 조정 가능
    max_page_size = 100  # 최대 페이지 크기 제한

# 게시글 목록 및 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by('-created_at')  # 최신순 정렬
        paginator = ArticlePagination()  # 페이지네이션 객체 생성
        result_page = paginator.paginate_queryset(articles, request)  # 요청에 따른 데이터 페이지 처리
        serializer = ArticleListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)  # 페이지네이션 응답 반환

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 게시글 상세정보 및 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != article.user:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user != article.user:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 댓글 목록 및 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 상세정보 및 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, article_id=article_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != comment.user:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if request.user != comment.user:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

