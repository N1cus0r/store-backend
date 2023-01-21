from django.urls import path
from . import views


urlpatterns = [
    path('create-order', views.CreateOrder .as_view()),
    path('create-product', views.CreateProduct.as_view()),
    path('get-filtered-products', views.GetFilteredProducts.as_view()),
    path('get-latest-products', views.GetLatestProducts.as_view()),
    path('get-related-products', views.GetRelatedProducts.as_view()),
    path('search-products', views.ProductSearch.as_view()),
]   