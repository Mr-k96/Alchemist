from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.comment_list_create),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.comment_detail),
]
