from django.urls import path 
from webhook import views 

urlpatterns = [ 
    # define a route for home 
    path('', views.webhook, name='webhook'), 
]