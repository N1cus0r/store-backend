from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter

from .serializers import ProductSerializer, CreateOrderSerializer
from .models import Product
from .pagination import FilteredProductsPagination, SearchPagination


class ProductSearch(ListCreateAPIView):
    pagination_class = SearchPagination
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["slug"]


class GetRelatedProducts(APIView):
    def get(self, request):
        category = request.query_params.get("category")
        brand = request.query_params.get("brand")
        slug = request.query_params.get("slug")

        if all((category, brand, slug)):
            related_products = Product.objects.filter(
                category=category, brand=brand
            ).exclude(slug=slug)[:12]
            serializer = ProductSerializer(related_products, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Query params were not provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetLatestProducts(APIView):
    def get(self, request):
        category = request.query_params.get("category")
        if category:
            products = Product.objects.filter(category=category)[:12]
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Category was not provided in params"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetFilteredProducts(APIView, FilteredProductsPagination):
    def get(self, request):
        category = request.query_params.get("category")
        brand = request.query_params.get("brand")
        slug = request.query_params.get("slug")
        query_params = (category, brand, slug)
        if any(query_params):
            filter = {}
            entries = zip(("category", "brand", "slug"), query_params)

            for key, value in entries:
                if value:
                    filter[key] = value

            queryset = Product.objects.filter(**filter)
            paginated_queryset = self.paginate_queryset(queryset, request, self)
            serializer = ProductSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(
            {"error": "Query filter were not provided in the params"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CreateProduct(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateOrder(APIView):
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
