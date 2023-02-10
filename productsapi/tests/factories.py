import random
import factory
from faker import Faker
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from productsapi.models import Product, Order, OrderItem


"""instance of Faker class that provides 
fake data for a SharedData instance"""

fake = Faker()

"""custom class which provider images temporary stored in memory
for SharedData instances and CustomUser instances"""


class ImageProvider:
    @staticmethod
    def get_model_field_image():
        image = Image.new(
            "RGBA",
            size=(50, 50),
            color=tuple(fake.pyint(min_value=0, max_value=225) for _ in range(3)),
        )
        file = BytesIO(image.tobytes())
        file.name = "test.png"
        file.seek(0)

        return ContentFile(file.read(), "test.png")

    @staticmethod
    def get_form_image():
        file = BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)
        return file


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    brand = fake.word()
    model = fake.word()
    color = fake.word()
    category = fake.word()
    price = fake.pyint(min_value=100, max_value=1000)
    sizes = [fake.pyint(min_value=40, max_value=45) for _ in range(5)]
    image = ImageProvider.get_model_field_image()


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    slug = "-".join([fake.word() for _ in range(5)])
    size = fake.pyint(min_value=40, max_value=45)
    price = fake.pyint(min_value=100, max_value=1000)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    full_name = fake.name()
    phone_number = fake.phone_number()
    email = fake.email()
    country = fake.country()
    city = fake.city()
    address = fake.street_address()
    item = factory.SubFactory(OrderItemFactory)
    payment_type = random.choice(["cash", "card"])
    total_price = factory.SelfAttribute("item.price")
