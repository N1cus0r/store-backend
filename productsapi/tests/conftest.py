import random
import pytest

from rest_framework.test import APIClient

from .factories import ImageProvider, ProductFactory, OrderFactory, fake


# provides a Product instance


@pytest.fixture
def new_product():
    return ProductFactory.create()


# provides form data for a Product instance


@pytest.fixture
def new_product_form_data():
    data = {
        "brand": fake.word(),
        "model": fake.word(),
        "color": fake.word(),
        "category": fake.word(),
        "price": fake.pyint(min_value=100, max_value=1000),
        "image": ImageProvider.get_form_image(),
        "sizes": [fake.pyint(min_value=40, max_value=45) for _ in range(5)],
    }

    return data


# provides an Order instance


@pytest.fixture
def new_order():
    return OrderFactory.create()


# provides form data for Order instance


@pytest.fixture
def new_order_form_data():
    data = {
        "full_name": fake.name(),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "country": fake.country(),
        "city": fake.city(),
        "address": fake.street_address(),
        "payment_type": random.choice(["cash", "card"]),
        "total_price": fake.pyint(min_value=10, max_value=100),
        "item": {
            "slug": "-".join([fake.word() for _ in range(5)]),
            "size": fake.pyint(min_value=40, max_value=45),
            "price": fake.pyint(min_value=100, max_value=1000),
        },
    }

    return data


@pytest.fixture
def api_client():
    return APIClient()
