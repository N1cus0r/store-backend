from django.urls import path
from . import views

app_name = "products"


urlpatterns = [
    path("create-order", views.CreateOrder.as_view(), name="create-order"),
    path("create-product", views.CreateProduct.as_view(), name="create-product"),
    path(
        "get-filtered-products",
        views.GetFilteredProducts.as_view(),
        name="get-filtered-products",
    ),
    path(
        "get-latest-products",
        views.GetLatestProducts.as_view(),
        name="get-latest-products",
    ),
    path(
        "get-related-products",
        views.GetRelatedProducts.as_view(),
        name="get-related-products",
    ),
    path("search-products", views.ProductSearch.as_view()),
]
