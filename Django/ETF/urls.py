from django.urls import path
from . import views


urlpatterns = [
    path('etf-list/', views.etf_list, name='etf-list'),
]