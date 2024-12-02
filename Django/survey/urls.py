# urls.py
from django.urls import path
from .views import get_questions
app_name = 'survey'

urlpatterns = [
    path('questions/', get_questions, name='get_questions'),
]