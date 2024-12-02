from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('', views.index, name='index'),
    # path('login/', views.login, name='login'),
    # path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('terms-agreement/', views.terms_agreement, name='terms_agreement'),
]