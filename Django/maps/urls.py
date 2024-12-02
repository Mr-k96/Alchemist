from django.urls import path
from . import views

app_name = 'maps'
urlpatterns = [
    path('get_nearby_banks/', views.get_nearby_banks, name='get_nearby_banks'),
]