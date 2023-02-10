from rest_framework import serializers

from .models import Product, Order, OrderItem

'''serializes the Product instance and generates 
a custom slug when instance created'''
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        image = serializers.ImageField()

        model = Product
        fields = [
            "id",
            "brand",
            "model",
            "color",
            "category",
            "slug",
            "price",
            "image",
            "time_created",
            "sizes",
        ]

    def create_slug(self, data):
        slug_lst = []
        for field in (data["brand"], data["model"], data["color"]):
            slug_lst.extend(list(map(lambda x: x.lower(), field.split())))
        return "-".join(slug_lst)

    def create(self, validated_data):
        validated_data["slug"] = self.create_slug(validated_data)
        return super().create(validated_data)

# serializes the OrderItem instance
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["slug", "size", "price"]

'''creates an Order instance and a OrderItem instance 
then populates total_price field with OrderItem price'''
class CreateOrderSerializer(serializers.ModelSerializer):
    item = OrderItemSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "full_name",
            "phone_number",
            "email",
            "country",
            "city",
            "address",
            "item",
            "payment_type",
            "time_created",
        ]

    def create(self, validated_data):
        order_item_data = dict(validated_data.pop("item"))

        order_item = OrderItem.objects.create(**order_item_data)

        total_price = order_item.price
        validated_data["total_price"] = total_price

        order = Order.objects.create(**validated_data)
        order.item = order_item
        order.save()

        return order
