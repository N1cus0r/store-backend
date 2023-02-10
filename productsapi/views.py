from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter

from .serializers import ProductSerializer, CreateOrderSerializer
from .models import Product
from .pagination import FilteredProductsPagination, SearchPagination


'''provides search functionality with pagination
of 6 objects per request''' 
class ProductSearch(ListAPIView):
    pagination_class = SearchPagination
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["slug"]

'''this view accepts GET requests and takes brand, category
and slug as query parameters, then return products with same
brand and category, it excludes the product with the slug provided '''
class GetRelatedProducts(APIView):
    def get(self, request):
        category = request.query_params.get("category")
        brand = request.query_params.get("brand")
        slug = request.query_params.get("slug")
        if all((category, brand, slug)):
            related_products = Product.objects.filter(
                category=category, brand=brand
            ).exclude(slug=slug)[:12]
            print(len(related_products))
            serializer = ProductSerializer(related_products, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Query params were not provided entirely"},
            status=status.HTTP_400_BAD_REQUEST,
        )

'''this view accept GET requests with category as query parameter
then returns 12 newest products from same category'''

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

'''this view accepts GET requests can take as query parameters
category, brand and slug then returns object filtered
by the parameter provided'''
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

'''this view accepts POST requests with form data
needed to create a ProductInstance'''
class CreateProduct(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

'''this view accepts POST requests with form data
needed to create a Order'''
class CreateOrder(APIView):
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
