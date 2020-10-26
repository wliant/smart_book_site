from django.shortcuts import render
from core.serializers import *
from core.migration_serializers import *
from core.models import *
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import filters


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


class BookViewSet(viewsets.ModelViewSet):
    filter_backends = (DynamicSearchFilter,)
    queryset = Book.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        return BookSerializer


class BookContentViewSet(viewsets.ModelViewSet):
    filter_backends = (DynamicSearchFilter,)
    queryset = BookContent.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        return BookContentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    filter_backends = (DynamicSearchFilter,)
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        return CategorySerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def migrate(request):
    data = JSONParser().parse(request)
    serializer = MigrationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(status=201)
    return JsonResponse(serializer.errors, status=400)
