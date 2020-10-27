from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
import json 
from django.shortcuts import render
from core.serializers import *
from core.migration_serializers import *
from core.models import *
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

@csrf_exempt 
def webhook(request): 
    # build a request object 
    req = json.loads(request.body) 
    # get intent name from json 
    intentName = req.get('queryResult').get('intent').get('displayName') 
    # return a fulfillment message 
    fulfillmentText = {'fulfillmentText': 'This is Django test response from webhook.'} 
    # return response 
    return JsonResponse(fulfillmentText, safe=False)