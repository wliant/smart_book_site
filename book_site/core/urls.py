from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views
from django.urls import path, include
from django.conf.urls import url


router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'bookContents', views.BookContentViewSet)
router.register(r'categorys', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path(r'migration/', views.migrate),
    path(r'api-auth/', include('rest_framework.urls')),
]
