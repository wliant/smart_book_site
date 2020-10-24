import requests
from flask import Flask, request, make_response, jsonify,send_file
from pydialogflow_fulfillment import DialogflowRequest
from pydialogflow_fulfillment import DialogflowResponse
from pydialogflow_fulfillment import SimpleResponse, Confirmation, OutputContexts, Suggestions
import GetBookRecommendations


app = Flask(__name__)

def getjson(url):
    resp = requests.get(url)
    print(url)
    return resp.json() 

# *****************************
# WEBHOOK MAIN ENDPOINT : START
# *****************************
PROJECT_ID = 'plp-smartbookguide-skb9'

@app.route('/', methods=['POST'])
def webhook():
    req = DialogflowRequest(request.data)
    intent_name = req.get_intent_displayName()
    print("here to print intent_name "+ intent_name)
    
    if intent_name == "GetRestaurantInfo" or intent_name == "ImageResponse": 
        return make_response(GetBookRecommendations.process(req))
    
    if intent_name == "Show me":
        return make_response(GetBookRecommendations.showResult(req))
        
    if intent_name == "GetRestaurantInfo - yes" or intent_name == "GetRestaurantInfo - yes - askSize"  or intent_name == "GetRestaurantInfo - yes - askDate" or intent_name == "GetRestaurantInfo - yes - askTime" or intent_name == "GetRestaurantInfo - yes - askLastName" or intent_name == "GetRestaurantInfo - yes - askFirstName" or intent_name == "GetRestaurantInfo - yes - askEmail" or intent_name == "GetRestaurantInfo - yes - askPhone":
        return make_response(GetBookRecommendations.makeReservation(req))
   
    if intent_name == "GetRestaurantInfo - no":
        return make_response(GetBookRecommendations.alternateResult(req))

    else:
        respose_text = "No intent matched from fullfilment code." 
    # Branching ends here
    
    # Finally sending this response to Dialogflow.
    return make_response(jsonify({"fulfillmentText": respose_text}))

  
@app.route('/image') 
def get_image():
    return send_file(request.args.get('path'), mimetype='image/gif') 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True) 
