from rest_framework.pagination import PageNumberPagination

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
    pagination_class = PageNumberPagination
    pagination_class.page_size = 30
    filter_backends = (DynamicSearchFilter,)
    queryset = Book.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return BookSerializer

    def retrieve(self, request, pk=None):
        super.retr


class BookContentViewSet(viewsets.ModelViewSet):
    filter_backends = (DynamicSearchFilter,)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    queryset = BookContent.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return BookContentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    pagination_class = None;
    filter_backends = (DynamicSearchFilter,)
    queryset = Category.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return CategorySerializer


class BookAccessViewSet(viewsets.ModelViewSet):
    filter_backends = (DynamicSearchFilter, )
    queryset = BookAccess.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return BookAccessSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def migrate(request):
    data = JSONParser().parse(request)
    serializer = MigrationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_auth(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
