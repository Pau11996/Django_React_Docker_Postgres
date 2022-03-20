from rest_framework import serializers

from ..models import Products, Category, Workshop


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):

    category = CategoryListSerializer()
    workshop = serializers.SlugRelatedField(slug_field='name', read_only='True')

    class Meta:
        model = Products
        fields = '__all__'



