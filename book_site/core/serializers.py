from core.models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class BookAccessSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BookAccess
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = ["id", "book", "content", "writer", "created"]


class BookSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(many=True, slug_field='name',
                                              queryset=Category.objects.all(), required=False)
    author = serializers.ReadOnlyField()


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
        fields = ["created", "name", "book_count"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(is_active=True, **validated_data)
        user.set_password(password)
        user.save()
        return user





