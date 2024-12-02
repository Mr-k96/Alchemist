"""
URL configuration for Archemist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import register  # 회원가입 뷰 함수 임포트
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('deposit/', include('deposit.urls')),
    path('ETF/', include('ETF.urls')),
    path('stock/', include('stock.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', register, name='rest_register'),
    path('survey/', include('survey.urls')),
    path('exchange_rate/', include('exchange_rate.urls')),
    path('maps/', include('maps.urls')),
    path('news/', include('news.urls')),
    path('ai_analysis/', include('ai_analysis.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
