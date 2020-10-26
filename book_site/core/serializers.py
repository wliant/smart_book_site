from core.models import Book, BookContent, Category
from rest_framework import serializers
from django.contrib.auth.models import User


class BookSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Book
        fields = "__all__"


class BookContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookContent
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)



