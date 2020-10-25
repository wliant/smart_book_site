from pydialogflow_fulfillment import DialogflowResponse
from pydialogflow_fulfillment import SimpleResponse, Confirmation, OutputContexts, Suggestions
import json
#import intelligence
#import MakeReservation
from multiprocessing import Pool


server_url = "https://61477f30.ngrok.io"

CONTEXT_ASK_PROGRAMME = "getrestaurantinfo-followup" 

CONTEXT_ASK_PROGRAMME_YES = "getrestaurantinfo-yes-followup"

def has_params(theKey, params):
    return theKey in params and params[theKey] != ""

def askDate(req):  
    res = DialogflowResponse("What is the date you are looking at?(e.g Date:dd/mm/yyyy)")
    print(req.get_parameters())
    res.add(SimpleResponse("What is the date you are looking at?(e.g Date:dd/mm/yyyy)","What is the date you are looking at?(e.g Date:dd/mm/yyyy)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response() 

def askTime(req): 
    res = DialogflowResponse("How about the time?(e.g Time:1730)")
    res.add(SimpleResponse("How about the time?(e.g Time:1730)","How about the time?(e.g Time:1730)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()
 
def askPartySize(req):
    res = DialogflowResponse("How many people?")
    res.add(SimpleResponse("How many people?","How many people?"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askfirstName(req):
    res = DialogflowResponse("May I know your first name?(e.g First Name:Sam)")
    res.add(SimpleResponse("May I know your first name?(e.g First Name:Sam)","May I know your first name?e.g First Name:Sam"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askLastName(req):
    res = DialogflowResponse("May I know your last name?(e.g Last Name:Lee)")
    res.add(SimpleResponse("May I know your last name?(e.g Last Name:Lee)","May I know your last name?(e.g Last Name:Lee)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askEmail(req):
    res = DialogflowResponse("What is your email address?(e.g Email:test@gmail.com)")
    res.add(SimpleResponse("What is your email address?(e.g Email:test@gmail.com)","What is your email address?(e.g Email:test@gmail.com)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def askPhone(req):
    res = DialogflowResponse("May I know your mobile number?(e.g Phone:83927594)")
    res.add(SimpleResponse("May I know your mobile number?(e.g Phone:83927594)","May I know your mobile number?(e.g Phone:83927594)"))
    res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME_YES,5,req.get_parameters()))
    return res.get_final_response()

def process(req):
    print("session id from process"+req.get_session_id()) 
    i = intelligence.Intel()
    if req.get_intent_displayName() == "ImageResponse" :
        queryId = int(req.get_parameters()["queryId"])
        # get req value parameter
        value = int(req.get_parameters()["value"])
        i.update_response(queryId, value, 0, 0)
    else:
        i.restart_query()
            
    print("session id from image response"+req.get_session_id())
    
    print(i.get_query_size())
    if i.get_query_size() >= 5: 
        id, path, restaurant_name = i.get_query()
     
        res = DialogflowResponse("We are recommending " + restaurant_name + ", please rate 1 - 5?")
        res.fulfillment_messages.append({
                "text": {
                    "text": [
                        "We are looking for the best restaurant for you. Please type \"Show me\" in 1 minute to show the result"
                    ]
                },
                "platform": "SLACK"
            })
        print("query size >=5")
        pool = Pool()
        pool.apply_async(i.calculate_result)
       
        print(res.get_final_response()) 
        return res.get_final_response() 
    else:
        id, path, restaurant_name = i.get_query()
     
        res = DialogflowResponse("We are recommanding " + restaurant_name + ", please rate 1 - 5?")
        res.fulfillment_messages.append({
            "card": { 
              "title": "We are recommanding " + restaurant_name + ", please rate 1 - 5?", 
              "imageUri": "{}/image?path={}".format(server_url, path), 
              "buttons": [ 
                {  
                  "text": 1,
                  "postback": "ImageResponse queryId {} value {}".format(id, 1) 
                },
                { 
                  "text": 2,
                  "postback": "ImageResponse queryId {} value {}".format(id, 2) 
                }, 
                { 
                  "text": 3,
                  "postback": "ImageResponse queryId {} value {}".format(id, 3) 
                }, 
                {
                  "text": 4, 
                  "postback": "ImageResponse queryId {} value {}".format(id, 4) 
                },
                {
                  "text": 5,
                  "postback": "ImageResponse queryId {} value {}".format(id, 5) 
                }
              ]
            },
            "platform": "SLACK"
          })  
       
        print(res.get_final_response()) 
        return res.get_final_response()   

def showResult(req):
    i = intelligence.Intel()

    if i.has_result():
        restaurant_name, image_url = i.get_result()
        res = DialogflowResponse("We are recommanding " + restaurant_name + ", do you want to make a reservation?")
        res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME,5,req.get_parameters()))
        res.fulfillment_messages.append({  
            "card": {
            "title": "We are recommanding " + restaurant_name + ", do you want to make a reservation?", 
            "imageUri": "{}/image?path={}".format(server_url,image_url[0]),
            "buttons": [ 
                {
                "text": "yes", 
                "postback": "yes:"+restaurant_name 
                },
                {
                    "text": "no",
                    "postback": "no"
                }
            ]
            }, 
            "platform": "SLACK" 
        })
    else:
        res = DialogflowResponse("No result found.")
        res.fulfillment_messages.append({  
                "text": {
                    "text": [
                        "No result found. You may type \"Find a restaurant\" to get another recommendation."
                    ]
                },
                "platform": "SLACK"
        })
    print(res.get_final_response()) 
    return res.get_final_response() 
def alternateResult(req):
    i = intelligence.Intel()
    if i.has_result():
        restaurant_name, image_url = i.get_result()
        res = DialogflowResponse("How about " + restaurant_name + ", do you want to make a reservation?")
        res.add(OutputContexts(req.get_project_id(), req.get_session_id(),CONTEXT_ASK_PROGRAMME,5,req.get_parameters()))
        res.fulfillment_messages.append({  
                "card": {
                "title": "How about " + restaurant_name + ", do you want to make a reservation?", 
                "imageUri": "{}/image?path={}".format(server_url,image_url[0]),
                "buttons": [ 
                    {
                    "text": "yes", 
                    "postback": "yes:"+restaurant_name 
                    },
                    {
                        "text": "no",
                        "postback": "no"
                    }
                ]
                },
                "platform": "SLACK" 
            })
        res.fulfillment_messages.append({  
            "text": {
                "text": [
                    "or you can type \"Find a restaurant\" to start again"
                ]
            },
            "platform": "SLACK"
        })
 
    else:
        res = DialogflowResponse("Thanks! You may type \"Find a restaurant\" to get another recommendation.")
        res.fulfillment_messages.append({
                "text": {
                    "text": [
                        "Thanks! You may type \"Find a restaurant\" to get another recommendation."
                    ]
                },
                "platform": "SLACK"
            })
    print(res.get_final_response()) 
    return res.get_final_response()
def makeReservation(req): 
    params = req.get_parameters()
    try:
        for con in req.get_ouputcontext_list(): 
            o_params = con["parameters"] 
            for x in o_params: 
                params[x] = o_params[x] 
    except: 
        None

    print("print params during init "+ str(params)) 
     
    if not has_params("date", params):
        print("here is not have date")
        return askDate(req)
    if not has_params("time", params):
        return askTime(req)    
    if not has_params("partySize", params):
        return askPartySize(req)
    if not has_params("firstName", params):
        return askfirstName(req)    
    if not has_params("lastName", params):
        return askLastName(req)
    if not has_params("email", params):
        return askEmail(req) 
    if not has_params("phoneNumber", params):
        return askPhone(req) 
 
 
    restaurant_name = "" if "restaurantName" not in params else params["restaurantName"]     
    reservation_date = "" if "date" not in params else params["date.original"] 
    reservation_time = "" if "time" not in params else params["time.original"]
    party_size = "" if "partySize" not in params else params["partySize.original"] 
    first_name = "" if "firstName" not in params else params["firstName"] 
    last_name = "" if "lastName" not in params else params["lastName"]
    email_address = "" if "email" not in params else params["email"]
    phone_number = "" if "phoneNumber" not in params else params["phoneNumber"] 
    
    
    MakeReservation.make_reservation(reservation_date,reservation_time,party_size,restaurant_name,first_name,last_name,email_address,phone_number)
    res = DialogflowResponse("finish making reservation for  " + restaurant_name )
       
    return res.get_final_response()

