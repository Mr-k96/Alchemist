from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("get-saved-news/", views.get_saved_news, name="get_saved_news"),
    path('save-news/', views.save_news, name='save_news'),
    path('get_news_list/', views.get_news_list, name='get_news_list'),
]
