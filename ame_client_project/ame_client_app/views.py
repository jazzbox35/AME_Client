#   Function:     This is a Django program for processing all REST transactions on the AME
#   Input:        User propositions and associated keywords 
#   Output:       Server evaluation of proposition and submission of a case for training in batch mode.

import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import logging
from ame_client_app.config import *

# Create list of submitted propositions held by the UX. 
propositions = {"proposition":[]}

logging.basicConfig(filename="ame_client_app.log",filemode='a',format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)

def index(request):
    # Display home screen
    global propositions
    data = {}
    next_action = 'display_home'
    return render(request, "ame_client_app/home.html", {"data": data, "next_action": next_action})

def CreateNewCase(request):
    global propositions
    
    api_url = 'https://' + AME_NODE + '.agiengine.online/createcase'
    headers = {
          'api-key':  AME_API_KEY
      }
    data = {}
    try:
        propositions ={"proposition":[]}
        response = requests.put(api_url, headers=headers, json=data)
    except:
        return HttpResponse("Cannot communicate with AME server")
    data = response.json()
    # stick the client list of propositions into the json data from the response
    data['propositions'] = propositions
    logging.info("CreateNewCase responding to html with>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)

def TrainCase(request):
    # Mark case for training -- but no further updates allowed
    global propositions
    case = request.GET.get('case')
    api_url = 'https://' + AME_NODE + '.agiengine.online/traincase'
    headers = {
          'api-key':  AME_API_KEY
      }
    #appearance =  request.GET.get('appearance')
    try:
        data = {
            "case": int(case),
        }
    except:
        data = {}
    
    try:
        response = requests.put(api_url, headers=headers, json=data)
    except:
        return HttpResponse("Cannot communicate with AME server")
    data = response.json()
    data['propositions'] = propositions
    logging.info("TrainCase responding to html with>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)

def AddProposition(request):
    global propositions

    case = request.GET.get('case')
    proposition = request.GET.get('proposition')
    appearance = request.GET.get('appearance')
    level = request.GET.get('level')
    system = request.GET.get('system')
    desired = request.GET.get('desired')


    api_url = 'https://' + AME_NODE + '.agiengine.online/sys' + system + '-proposition'
    headers = {
          'api-key':  AME_API_KEY
      }
    
    try:
        data = {
          "case": int(case),
          "proposition" :  proposition,
          "appearance"  :  appearance,
          "essence"     : "",
          "level"       : int(level),
          "desired"     :  desired,
          "system"      : system
        }
    except:
        data ={}

    # call the ame
    try:    
        response = requests.put(api_url, headers=headers, json=data)
        if type(response.status_code) == int and response.status_code == 200:
            # add new proposition to front of client proposition list -- this is only used by the client UX
            propositions["proposition"].insert(0,data)
            logging.info("added to propositions>" + str(data))
        else:
            logging.info("NOT adding to propositions due to return code>" + str(data))
        data = response.json()
    except:
        return HttpResponse("Cannot communicate with AME server")
    
    # stick the client list of propositions into the json data from the response
    data['propositions'] = propositions

    """ INSERT CODE HERE IF YOU WISH TO CREATE A DEFAULT VALUE FOR THE NEXT PROPOSITION BASED ON THE PROPOSITION JUST SUBMITTED ABOVE.
    FOR EXAMPLE IF THE PROPOSITION POSTED ABOVE IS LEVEL 0, SYSTEM 1 (L0 AND S1), AND THE PROPOSITION WAS 'CAR IS MOVING',
    AND THE APPEARANCE IS 'FAST', THEN PERHAPS ASSIGN 'CAR DRIVING RECKLESSLY' AS THE DEFAULT LEVEL 1, SYSTEM 1 JUDGMENT.
     """
    
    logging.info("AddProposition responding to html with>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)

def Deliberate(request):
    global propositions
    
    # don't call the ame unless the most recent proposition (main idea) is System 2!
    if propositions["proposition"][0]["system"] == '2':
        pass
    else:
        # The ame should reject these but this will suffice
        data = {}
        data['decision'] = ["ERROR -- Last proposition must be System 2 and Level 1 or Level 2."]
        data['judgments'] = [[]]
        return JsonResponse(data)
 
    case = request.GET.get('case')
    api_url = 'https://' + AME_NODE + '.agiengine.online/sys2-realistic'
    headers = {
          'api-key':  AME_API_KEY
      }
    
    try:
        data = {
          "case": int(case),
        }
    except:
        data = {}
    
    try:
        response = requests.put(api_url, headers=headers, json=data)
    except:
        return HttpResponse("Cannot communicate with AME server")
    data = response.json()
    data['propositions'] = propositions
    logging.info("Deliberate responding to html with>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)

def RetractProposition(request):
    # Retract the most recent proposition
    global propositions

    case = request.GET.get('case')
    api_url = 'https://' + AME_NODE + '.agiengine.online/retract_that'
    headers = {
          'api-key':  AME_API_KEY
      }

    try:
        data = {
          "case": int(case),
        }
    except:
        data ={}

    try:            
        response = requests.put(api_url, headers=headers, json=data)
        if type(response.status_code) == int and response.status_code == 200:
            # propositions is type {} with entry "proposition" which points to a type []. 
            # The list is the propositions submitted by the client.
            if len(propositions["proposition"]) > 1:
                propositions["proposition"] = propositions["proposition"][1:]
            else:
                propositions["proposition"] = []
    except:
        return HttpResponse("Cannot communicate with AME server")
    data = response.json()
    data['propositions'] = propositions
    logging.info("RetractProposition responding to html with>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)

