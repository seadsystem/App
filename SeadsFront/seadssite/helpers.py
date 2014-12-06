import ast
import requests
from dateutil.parser import *
from .models import Devices, Map
import time

'''
format for API calls
'''

def get_plug_data(start_time, end_time, dtype, device_id):
    #the basic API call will have a base format that includes just a device ID, it builds from that
    api_string = "http://128.114.59.76:8080/{}".format(device_id)
    #the next optional appendage to the API call is dtype which can be I,V or W (current, volt or watt)
    api_string += "?type={}".format(dtype)  
    #the next optional appendage to the API call is start and end time
    api_string += "&start_time={}&end_time={}".format(start_time, end_time)
    #the current strategy is to create subsets by dropping certain points -- to be worked on
    api_string += "&subset={}".format(100)
    #following is for testing purposes -- seing how long API calls take etc
    print "API CALL: {}".format(api_string)
    start = time.time()
    api_response = requests.get(api_string).text
    end = time.time()
    print "API Took: {}seconds".format(end-start)
    start = time.time()
    api_response = ast.literal_eval(api_response)
    for row in api_response:
        for index, value in enumerate(row):
            if index > 0 and value not in [dtype]:
                row[index] = int(value)
    end = time.time()
    print "Server Processing Took: {}seconds".format(end-start)
    return api_response


def delete_device(device_id, current_user):
    D = Devices.objects.filter(device_id = device_id)
    M = Map.objects.filter(device=D)
    #if the user owns the device they are trying to delete
    if Map.objects.filter(user=current_user.id, device=D):
        Devices.objects.filter(device_id = device_id).delete()
    else:
        return "you don't own the device you're deleting, or it doesn't exist"
    return None


def register_device(device_id, device_name, current_user):
    #check if device is already registered to this user
    D = Devices.objects.filter(device_id=device_id)
    if Map.objects.filter(user=current_user.id, device=D):
        return "The device you've attempted to register has already been registered."
    else:
    #try to create a new device and map it to the user
        try:
            D = Devices(device_id=device_id, name=device_name)
            D.save()     
            Map(user = current_user, device = D).save()
        #catch errors
        except ValueError:
            print "Invalid Device ID"
        except TypeError:
            print "Invalid Device ID"
    return None


def modify_device_name(device_id, name):
        '''
        a bit of a hack, this assumes every device has a unique ID, will have to be enforced in DB
        we must also enforce that the name field can't be blank
        '''
        #save info to device object
        D = Devices.objects.filter(device_id = device_id)[0]        
        D.name = new_name
        D.save()
