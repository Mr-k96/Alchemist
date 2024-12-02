from django.urls import path
from . import views

app_name = "stock"

urlpatterns = [
    path("stock-data/", views.get_stock_data, name="stock_data"),
]
