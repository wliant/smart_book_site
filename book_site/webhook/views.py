from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from core.serializers import *
from core.migration_serializers import *
from core.models import *
from webhook.df_response_lib import *
from core.recommendation_engine.recommender import *
from core.sentiment_analysis import *

recommender = RecommendationEngine()

@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)

    list_of_books = []
    print('get popular book recommendation: ')
    list_of_books = recommender.get_popular_recommendation(
        length=10, samples=5000)
    
    # get intent name from json
    fulfillmentText = 'This is Django test response from webhook.'
    intent_name = req.get('queryResult').get('intent').get('displayName')
    print("here to print intent_name " + intent_name)

    ff_response = fulfillment_response()
    contexts = []
    if intent_name == 'GetBooksRead':
        fulfillmentText = 'Hi Adam, you have read ' + \
            str(len(BookAccess.objects.filter(user_id='1')))+' books.'

    if intent_name == 'GetGeneralRecommendation':
        fulfillmentText = 'Sure, what category of books would you like?'
        contexts = [
            ['getgeneralrecommendation-followup', 2, {'parameter': ''}]]

    if intent_name == 'GetGeneralRecommendation - GetGenre':
        cat = req.get('queryResult').get('queryText')

        if str(cat).lower() != 'anything':
            print('get user preferred book recommendation: ')
            print(recommender.get_recommendation_by_categories(
                categories=[cat], length=10))
            list_of_books = recommender.get_recommendation_by_categories(categories=[bookgenre], length=10)

        fulfillmentText = 'Alright, we found ' + str(len(list_of_books)) + ' books to recommend, they are: '+str(list_of_books)

    if intent_name == 'GetGenreSpecificRecommendations':
        mess = req.get('queryResult').get("outputContexts")
        params = mess[0].get("parameters")
        bookgenre = params["bookgenre"]
        print(bookgenre)
        print('get user preferred book recommendation: ')
        list_of_books = recommender.get_recommendation_by_categories(categories=[bookgenre], length=10)

        fulfillmentText = 'Alright, here are some ' + bookgenre + \
            ' books for you to consider:' + str(list_of_books)

    if intent_name == 'writeReview':
        fulfillmentText = 'Hi, Adam. Sure, what is the title of the book?(e.g the title of the book is \'abc\')'
        contexts = [['writereview-followup', 2, {'parameter': ''}]]

    if intent_name == 'writeReview - getTitle':
        mess = req.get('queryResult').get("outputContexts")
        params = mess[0].get("parameters")
        title = params["title"]
        try:
            book = Book.objects.get(title=title)
        except:
            fulfillmentText = 'Sorry, this book is not in our library.'
            session = req.get("session")
            ff_out_context = ff_response.output_contexts(session, contexts)
            ff_text = ff_response.fulfillment_text(fulfillmentText)
            reply = ff_response.main_response(
                fulfillment_text=ff_text, output_contexts=ff_out_context)
            return JsonResponse(reply, safe=False)
        fulfillmentText = 'Ok got it. What do you have to say about the book?(Please start the review with I think)'
        contexts = [
            ['writereview-gettitle-followup', 2, {'parameter': params}]]

    if intent_name == 'writeReview - getTitle - review':
        review = req.get('queryResult').get('queryText')
        evaluate = evaluate_review_text(review)[2]
        print(evaluate_review_text(review))
        params = {}
        mess = req.get('queryResult').get("outputContexts")
        params = mess[1].get("parameters")
        title = params["title"]
        book = Book.objects.get(title=title)
        book_id = Book._meta.get_field('id').value_from_object(book)
        writer = "Adam"
        r = Review(writer=writer, content=review, book_id=book_id)
        r.save()
        if evaluate == 'positive':
            fulfillmentText = 'Nice, you have a positive opinion about the book, it seems you like the author and the overall book. Would you like us to recommend similar books?(yes/no)'
        else:
            fulfillmentText = 'Oh no, it seems like you didn’t like the book. Would you like us to recommend you other books, hopefully you’ll enjoy those better!(yes/no)'
        contexts = [
            ['writereview-gettitle-review-followup', 2, {'parameter': params}]]

    if intent_name == 'writeReview - getTitle - review - yes':
        print('get popular book recommendation: ')
        fulfillmentText = 'Alright, we found ' + \
            str(len(list_of_books)) + \
            ' books to recommend, they are: '+str(list_of_books)

    # get session name from fulfilment reqest
    session = req.get("session")
    # set the output context in the webhook response
    ff_out_context = ff_response.output_contexts(session, contexts)
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    reply = ff_response.main_response(
        fulfillment_text=ff_text, output_contexts=ff_out_context)
    return JsonResponse(reply, safe=False)
