from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from core.serializers import *
from core.migration_serializers import *
from core.models import *
from webhook.df_response_lib import *
#from core.recommendation import *
# from core.sentiment_analysis import *

@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    
    # get intent name from json
    fulfillmentText = {
        'fulfillmentText': 'This is Django test response from webhook.'}
    intent_name = req.get('queryResult').get('intent').get('displayName')
    print("here to print intent_name " + intent_name)

    ff_response = fulfillment_response()
    contexts = []
    if intent_name == 'GetBooksRead':
        fulfillmentText = 'Hi Adam, you have read ' + str(len(BookAccess.objects.filter(user_id='1')))+' books.'
    
    if intent_name == 'GetTopGenre':
        fulfillmentText = 'You favourite category of books is horror, you have read 12 horror books. Would you like me to recommend you a horror book?'
        contexts = [['gettopgenre-followup', 2, {'parameter': ''}]]

    if intent_name == 'GetTopGenre - yes':
        fulfillmentText = 'Based on your reading history, we’d like to recommend you XX horror book'
    
    if intent_name == 'GetGeneralRecommendation':
        fulfillmentText = 'Sure, what category of books would you like?'
        contexts = [['getgeneralrecommendation-followup', 2, {'parameter': ''}]]

    if intent_name == 'GetGeneralRecommendation - GetGenre':
        fulfillmentText = 'Alright, we found XX books to recommend, they are: '
    
    if intent_name == 'writeReview':

        fulfillmentText = 'Hi, Adam. Sure, what is the title of the book?'
        contexts = [['writereview-followup', 2, {'parameter': ''}]]

    if intent_name == 'writeReview - getTitle':
        print(req)
        mess = req.get('queryResult').get("outputContexts")
        params = mess[0].get("parameters")
        print(params)
        title = params["title"]
        print(title)
        try:
            book = Book.objects.get(title=title)
        except :
            fulfillmentText = 'Sorry, this book is not in our library.'
            session = req.get("session")
            ff_out_context  = ff_response.output_contexts(session, contexts)
            ff_text = ff_response.fulfillment_text(fulfillmentText)
            print(ff_out_context)
            reply = ff_response.main_response(fulfillment_text = ff_text, output_contexts = ff_out_context)
            return JsonResponse(reply, safe=False)
        fulfillmentText = 'Ok got it. What do you have to say about the book?'
        contexts = [['writereview-gettitle-followup', 2, {'parameter': params}]]

    if intent_name == 'writeReview - getTitle - review':
        print(req)
        review = req.get('queryResult').get('queryText')
        print(review)
        print(req)
        params = {}
        mess = req.get('queryResult').get("outputContexts")
        params = mess[1].get("parameters")
        print(params)
        title = params["title"]
        print(title)
        book = Book.objects.get(title=title)
        book_id = Book._meta.get_field('id').value_from_object(book)
        writer = Book._meta.get_field('author').value_from_object(book)
        print(book_id)
        print(writer)
        r = Review(writer=writer,content=review, book_id= book_id)
        r.save()
        fulfillmentText = 'Nice, you have a positive opinion about the book, it seems you like the author and the overall book. Would you like us to recommend similar books?'
        contexts = [['writereview-gettitle-review-followup', 2, {'parameter': params}]]

    # print(evaluate_review_text("it is a good book"))
    # get session name from fulfilment reqest
    session = req.get("session")
    print(session)
    # set the output context in the webhook response
    ff_out_context  = ff_response.output_contexts(session, contexts)
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    print(ff_out_context)
    reply = ff_response.main_response(fulfillment_text = ff_text, output_contexts = ff_out_context)
    return JsonResponse(reply, safe=False)
