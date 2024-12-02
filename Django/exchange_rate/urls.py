from django.urls import path
from . import views

app_name = 'exchange_rate'
urlpatterns = [
    path('', views.get_exchange_rate, name='get_exchange_rate'),
]