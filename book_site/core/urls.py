from rest_framework.routers import DefaultRouter
from core import views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'bookContents', views.BookContentViewSet)
router.register(r'bookAccesses', views.BookAccessViewSet)
router.register(r'categorys', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'migration/', views.migrate),
    path(r'auth/signup/', views.create_auth),
    path(r'auth/token/', obtain_auth_token),
]
