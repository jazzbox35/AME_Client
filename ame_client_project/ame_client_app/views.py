#   Function:     \This is a Django program for processing all REST transactions on the AME
#   Input:        User propositions and associated keywords 
#   Output:       Server evaluation of proposition and submission of a case for training in batch mode.

import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import logging
from ame_client_app.config import *

logging.basicConfig(filename="ame_client_app.log",filemode='a',format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)

def index(request):
    # Display home screen
    data = {}
    next_action = 'display_home'
    return render(request, "ame_client_app/home.html", {"data": data, "next_action": next_action})

def CreateNewCase(request):
    # Mark case for training -- but no further updates allowed
    api_url = 'https://' + AME_NODE + '.agiengine.online/createcase'
    headers = {
          'api-key':  AME_API_KEY
      }
    data = {}
    try:
        response = requests.put(api_url, headers=headers, json=data)
    except:
        return HttpResponse("Cannot communicate with AME server")
    data = response.json()
    logging.info("create case>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)

def TrainCase(request):
    # Mark case for training -- but no further updates allowed
    case = request.GET.get('case')
    api_url = 'https://' + AME_NODE + '.agiengine.online/traincase'
    headers = {
          'api-key':  AME_API_KEY
      }
    #appearance =  request.GET.get('appearance')
    data = {
      "case": int(case),
    }
    
    try:
        response = requests.put(api_url, headers=headers, json=data)
    except:
        return HttpResponse("Cannot communicate with AME server")
    data = response.json()
    logging.info("train case>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)

def AddProposition(request):
    
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
    
    data = {
      "case": int(case),
      "proposition" :  proposition,
      "appearance"  :  appearance,
      "essence"     : "",
      "level"       : int(level),
      "desired"     :  desired
    }
    logging.info(data)
    try:
        response = requests.put(api_url, headers=headers, json=data)
    except:
        return HttpResponse("Cannot communicate with AME server")
    data = response.json()
    logging.info("proposition>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)


def Deliberate(request):
    # Create level 1, system 2 judgment(s) and post to the server
    case = request.GET.get('case')
    api_url = 'https://' + AME_NODE + '.agiengine.online/sys2-realistic'
    headers = {
          'api-key':  AME_API_KEY
      }
    #appearance =  request.GET.get('appearance')
    data = {
      "case": int(case),
    }
    
    try:
        response = requests.put(api_url, headers=headers, json=data)
    except:
        return HttpResponse("Cannot communicate with AME server")
    data = response.json()
    logging.info("realistic call>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)

def RetractProposition(request):
    # Retract the most recent proposition
    case = request.GET.get('case')
    api_url = 'https://' + AME_NODE + '.agiengine.online/retract_that'
    headers = {
          'api-key':  AME_API_KEY
      }
    data = {
      "case": int(case),
    }
    
    try:
        response = requests.put(api_url, headers=headers, json=data)
    except:
        return HttpResponse("Cannot communicate with AME server")
    data = response.json()
    logging.info("retract that>" + str(data) + " status>" + str(response.status_code))
    return JsonResponse(data)

