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
from core.recommendation_engine.recommender import *
from core.classification import classify


recommender = RecommendationEngine()


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


class BookViewSet(viewsets.ModelViewSet):
    filter_backends = (DynamicSearchFilter,)
    queryset = Book.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return BookSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username)


class BookContentViewSet(viewsets.ModelViewSet):
    filter_backends = (DynamicSearchFilter,)
    queryset = BookContent.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return BookContentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    filter_backends = (DynamicSearchFilter,)
    queryset = Review.objects.all()
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user.username)


class CategoryViewSet(viewsets.ModelViewSet):
    pagination_class = None
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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_recommendation(request):

    #print('get popular book recommendation: ')
    #titles = recommender.get_popular_recommendation(length = 4, samples = 5000)
    #print('get user preferred book recommendation: ')
    #titles = recommender.get_recommendation_by_categories(categories=['romance'], length = 10)

    #books = Book.objects.filter(title__in=titles)
    books = Book.objects.all().order_by("-views")[:4]
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def categorize(request):
    book_id = request.query_params["book"]
    classify(book_id)
    print("categorized")
    return HttpResponse(status=200)
