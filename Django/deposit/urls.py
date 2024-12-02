from django.urls import path
from . import views

app_name = 'deposit'

urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products, name='save-deposit-products'),
    path('deposit-products/', views.get_all_deposit_products, name='get-deposit-products'),
    path('deposit-products/<str:fin_prdt_cd>/', views.get_deposit_product_detail, name='get-deposit-product-detail'),
]
