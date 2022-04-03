from rest_framework.response import Response
from rest_framework import viewsets, serializers, permissions
from rest_framework.views import APIView

from .serializers import (
    ProductsSerializer,
    CategoryListSerializer
)

from ..models import Products, Category


# class CategoryViewSet(viewsets.ModelViewSet):
#
#     queryset = Category.objects.all()
#     serializer_class = CategoryDetailSerializer

class CategoryListView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        category = Category.objects.all()
        serializer = CategoryListSerializer(category, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView):

    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategoryListSerializer(category, many=False)
        return Response(serializer.data)


# class ProductListView(APIView):
#
#     def get(self, request):
#         products = Products.objects.all
#         serializer = ProductsSerializer(products, many=True)
#         return Response(serializer.data)


class ProductsViewSet(viewsets.ModelViewSet):

    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [permissions.IsAuthenticated]


# View for reviews in future

# class ReviewCreateView(APIView):
#     """Добавление отзыва к товарам"""
#
#     def post(self, request, ):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)


