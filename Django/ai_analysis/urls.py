from django.urls import path
from . import views

urlpatterns = [
    path('analysis/', views.ai_analysis, name='ai_analysis'),
]