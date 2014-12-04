import ast
import requests
from .models import Devices, Map
import time


def get_connected_devices(maps):
    if len(maps) == 0:
        return 0
    connected_devices = 0
    for dmap in maps:
        if dmap.device.connection:
            connected_devices += 1
    return connected_devices


def get_max_power_usage(minutes, maps):
    if len(maps) == 0:
        return 0
    current_power_usage = 0
    now = int(time.time())
    then = now - (minutes * 60)
    for dmap in maps:
        usage = get_plug_data(then, now, "W", dmap.device.device_id)
        if len(usage) < 2:
            continue
        current_power_usage += max(usage[1:], key=lambda x:x[1])[1]
    return current_power_usage / len(maps)


def get_average_power_usage(minutes, maps, samples):
    if len(maps) == 0:
        return 0
    average_power_usage = 0
    now = int(time.time())
    then = now - (minutes * 60)
    hours = minutes / 60
    samp_hr = samples/hours

    for dmap in maps:
        usage = get_plug_data(then, now, "W", dmap.device.device_id, samples)
        if len(usage) < 2:
            continue
        average_power_usage += ((sum(map(lambda x:x[1], usage[1:]))/len(usage[1:])) * samp_hr)
    return int(average_power_usage / len(maps))


def get_plug_data(start_time, end_time, dtype, device_id, samples = 100):
    api_string = "http://128.114.59.76:8080/{}".format(device_id)
    api_string += "?type={}".format(dtype)  
    api_string += "&start_time={}&end_time={}".format(start_time, end_time)
    api_string += "&subset={}".format(samples)
    print "API CALL: {}".format(api_string)
    #start = time.time()
    api_response = requests.get(api_string).text
    #end = time.time()
    #print "API Took: {}seconds".format(end-start)
    #start = time.time()
    api_response = ast.literal_eval(api_response)
    for row in api_response:
        for index, value in enumerate(row):
            if index > 0 and value not in [dtype]:
                row[index] = int(value)
    #end = time.time()
    #print "Server Processing Took: {}seconds".format(end-start)
    #print api_response
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
