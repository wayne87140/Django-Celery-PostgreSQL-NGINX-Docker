from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import json

from main.utils.IPandCOM import IPCOMform
from main.utils.login_decorator import customed_login_required

from account.models import User
from main.models import TaskResult
from favorite.models import FavoriteDevice

# Create your views here.
@customed_login_required
@never_cache
def favorite(request):
    currentuser = request.user
    
    if not currentuser.is_authenticated:
        return HttpResponse('The password has already modified. Please reload page and re-login.')  
     
    latest_result = TaskResult.objects.latest('pubDateTime')
    tablejson = latest_result.devices_with_tableHTML
    devicetable = json.loads(tablejson)
    
    disabledevices = json.loads(User.objects.get(username=currentuser).DisableList)
    
    devices = currentuser.favoritedevice_set.all()

    favoritedevices = [x.device_IP for x in devices]
    # ex:['127.0.0.1_4001','127.0.0.1_4002','COM5_1',...]
    
    fav_without_dis = list(device for device in favoritedevices if device not in disabledevices)
        
    tablehtml=''
    for IPPort in fav_without_dis:
        tablehtml_each = devicetable.get(IPPort)
        if tablehtml_each:
            tablehtml+=tablehtml_each
    context = {"tablestr":tablehtml}
    
    if request.is_ajax():
        return render(request, 'main/content.html', context)     
    return render(request, 'favorite/favorite.html', context)


@login_required
def settings(request):
    currentuser = request.user
    default_access = User.objects.get(username=currentuser).Default_Access
    availablelist = json.loads(User.objects.get(username=currentuser).AvailableList)
    
    if (default_access==False) and not availablelist:
        return render(request, 'favorite/settings.html', {'devicesform':''})
    
    current_IP = json.loads(TaskResult.objects.latest('pubDateTime').connectinIP)
    # current_IP is a dictionary {'IP: 'Type Name', ...}
    
    disabledevices = json.loads(User.objects.get(username=currentuser).DisableList)
    devices = currentuser.favoritedevice_set.all()
    favoritedevices = {device.device_IP: (current_IP.get(device.device_IP, None),) for device in devices}
    
    if request.method=='GET':
        devicesform = IPCOMform(current_IP, favoritedevices, disabledevices)
        context = {'devicesform':devicesform}
        return render(request, 'favorite/settings.html', context)
    
    
    if request.method=="POST":    
        for favorite_device in favoritedevices:
            if favorite_device not in request.POST:
                removed_device = FavoriteDevice.objects.get(device_IP = favorite_device)
                removed_device.IPlikes.remove(currentuser)
                removed_device.save()
                
        for checkedIP in request.POST:
            if 'csrf' not in checkedIP:   # exclude csrf token     
                updateDevice = FavoriteDevice.objects.get_or_create(
                    device_IP = checkedIP)
                ## updateDevice returns a tuple
                updateDevice[0].IPlikes.add(currentuser) 
                updateDevice[0].save()
                          
    messages.success(request, 'Favorite updated successfully!')
    return redirect('favorite:favorite')







