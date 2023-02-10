import pytest

from productsapi.models import Product, Order

#testing hte creation of and instance of Product model

@pytest.mark.django_db
def test_create_product_model(new_product):
    assert Product.objects.count() == 1

    last_created = Product.objects.last()

    assert last_created.id == new_product.id

    assert str(last_created) == new_product.slug

#testing hte creation of and instance of Order model

@pytest.mark.django_db
def test_create_order_item_model(new_order):
    assert Order.objects.count() == 1

    last_created = Order.objects.last()

    assert last_created.id == new_order.id
