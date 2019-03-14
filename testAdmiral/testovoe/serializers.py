from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Стандартный сериалайзер для модели
    """
    class Meta:
        model = Category
        fields = '__all__'
