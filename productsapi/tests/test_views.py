import pytest

from django.urls import reverse

from productsapi.models import Product, Order
from .factories import ProductFactory, fake

"""testing the retrieving of newest 12 products by providing 
category to filter, from the API endpoint via GET request"""

@pytest.mark.django_db
def test_get_related_products_view(new_product, api_client):
    empty_response = api_client.get(
        path=reverse("products:get-related-products"),
        data={
            "category": new_product.category,
            "brand": new_product.brand,
            "slug": new_product.slug,
        },
    )

    assert empty_response.status_code == 200

    assert empty_response.data == []

    ProductFactory.create(model=fake.word(), color=fake.word())

    loaded_response = api_client.get(
        path=reverse("products:get-related-products"),
        data={
            "category": new_product.category,
            "brand": new_product.brand,
            "slug": new_product.slug,
        },
    )

    assert loaded_response.status_code == 200

    assert len(loaded_response.data) == 1


"""testing the retrieving of last 12 products by providing 
category to filter, from the API endpoint via GET request"""

@pytest.mark.django_db
def test_get_latest_products_view(new_product, api_client):
    ProductFactory.create_batch(size=12, category=new_product.category)

    response = api_client.get(
        path=reverse("products:get-latest-products"),
        data={"category": new_product.category},
    )

    assert response.status_code == 200

    assert len(response.data) == 12

"""testing the retrieving of filtered products by providing 
fields to filter, from the API endpoint via GET request"""

@pytest.mark.django_db
def test_get_filtered_products_view(api_client):
    unique_category = fake.word()
    unique_brand = fake.word()
    ProductFactory.create_batch(size=13, category=unique_category)
    ProductFactory.create_batch(size=13, category=unique_category)
    ProductFactory.create_batch(size=13, category=unique_category, brand=unique_brand)

    category_filter_response = api_client.get(
        path=reverse("products:get-filtered-products"),
        data={"category": unique_category},
    )

    brand_filter_response = api_client.get(
        path=reverse("products:get-filtered-products"), data={"brand": unique_brand}
    )

    mixed_filter_response = api_client.get(
        path=reverse("products:get-filtered-products"),
        data={"category": unique_category, "brand": unique_brand},
    )

    assert category_filter_response.status_code == 200

    assert brand_filter_response.status_code == 200

    assert mixed_filter_response.status_code == 200

    assert len(category_filter_response.data.get("results")) == 12

    assert len(brand_filter_response.data.get("results")) == 12

    assert len(mixed_filter_response.data.get("results")) == 12

"""testing the creation of a Product instance from
the API endpoint via POST request"""

@pytest.mark.django_db
def test_create_product_view(new_product_form_data, api_client):
    response = api_client.post(
        path=reverse("products:create-product"), data=new_product_form_data
    )

    assert response.status_code == 201

    assert Product.objects.count() == 1

"""testing the creation of a Order instance from
the API endpoint via POST request"""

@pytest.mark.django_db
def test_create_order_view(new_order_form_data, api_client):
    response = api_client.post(
        path=reverse("products:create-order"), data=new_order_form_data, format="json"
    )

    assert response.status_code == 201

    assert Order.objects.count() == 1
