from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta
import json

from account.models import User
from main.models import TaskResult
from main.utils.DataExtraction import Extraction
from main.utils.login_decorator import customed_login_required
from search.models import T_H_Image
from search.utils.plot import Plot


# Create your views here.
@customed_login_required
def search(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse('The password has already modified. Please reload page and re-login.') 
    
    extraction = Extraction() 
       
    default_access = User.objects.get(username=current_user).Default_Access
    availablelist = json.loads(User.objects.get(username=current_user).AvailableList)
    
    if (default_access==False) and not availablelist: # This is for the situation that all devices are disabled.
        return render(request, 'search/search.html', {'tablestr':''})
    
    disablelist = json.loads(User.objects.get(username=current_user).DisableList)   
    
    IPCOMwithD = request.GET.get('search')
    if IPCOMwithD:
        IPCOMwithD = IPCOMwithD.upper()
        request.session['searchresult'] = IPCOMwithD
    else: 
        IPCOMwithD = request.session['searchresult'].upper()        
    IPCOM = IPCOMwithD.split('/')[0]   # the return formats are "127.0.0.1_12/THS" or "THS" or "OFFLINE"
        
    latest_result = TaskResult.objects.latest('pubDateTime')
    current_results = latest_result.devices_with_tableHTML
    connectinIP = latest_result.connectinIP
    
    current_results = json.loads(current_results)   # current_results = {'IP_Port': 'table_html', ...}
    connectinIP = json.loads(connectinIP)           # connetinIP= {'IP_Port': 'Type', ...}
    
    for disable_device in disablelist:
        connectinIP.pop(disable_device, None)

    specificDevicenumber = extraction.NamewithTypeNum.get(IPCOMwithD) # if the IPCOMwithD is Device name

    if request.is_ajax():
        template_location = 'main/content.html'
    else: 
        template_location = 'search/search.html'
        
    if specificDevicenumber: 
        # This is for the case of searching Device Type, included OFFLINE
        TypeSearched = IPCOMwithD
        htmlstring = ''
        for IPPORT, Type in connectinIP.items():
            if Type ==TypeSearched:
                htmlstring+=current_results.get(IPPORT)
        context = {'tablestr':htmlstring}
        return render(request, template_location, context)
                    
    if connectinIP.get(IPCOM):   
        # This is for the case of searching specific IPwithPort
        htmlstring = current_results.get(IPCOM)
        context = {'tablestr':htmlstring}
        return render(request, template_location, context)
    
    return HttpResponse("sorry the device is not found. Or, you don't have the authority")

@login_required
def plot(request, IPorCOM):
    image_item = None
    dayBeforeNow = datetime.now()-timedelta(hours=23)
    start_datehour = dayBeforeNow.strftime('%Y.%m.%d.%H')

    plot = Plot(IPorCOM, start_datehour, '24')
    result = plot.plot_figure()
    chartjsvariables = plot.get_ChartjsVariables()
    if result:
        imagename = result[0]
        content_file = result[1]
        try:
            image_item = T_H_Image.objects.get(image_name = imagename)
            image_item.image.save(imagename+'.png', content_file)
            image_item.save()
        except T_H_Image.DoesNotExist:
            image_item = T_H_Image()
            image_item.image_name = imagename
            image_item.image.save(imagename+'.png', content_file)
            image_item.save()
        
    context = {'IPorCOM':IPorCOM, 'img':image_item, 
               'start_datehour':start_datehour, 'chartjsvariables':chartjsvariables}         
    return render(request, 'search/plot.html', context)        
           

@login_required
def findplot(request):
    image_item = None
     
    start_datehour = request.POST.get('start_time') # 20YY.MM.DD.HH
    total_hour = request.POST.get('total_hour')     # '1'~'24'
    IPorCOM = request.POST.get('IPorCOM')   
    
    # T_H_image.image_name = 127.0.0.1_2020.09.08.15_24
    imagename = IPorCOM+'_'+start_datehour+'_'+total_hour        
    try:    
        image_item = T_H_Image.objects.get(image_name = imagename)
        
        end_datehour = datetime.strptime(start_datehour, "%Y.%m.%d.%H")\
                        +timedelta(hours=int(total_hour))
        datetime_now = datetime.now()
        
        if end_datehour>datetime_now:
        #Refresh the picture up-to-date
            plot = Plot(IPorCOM, start_datehour, total_hour)
            result = plot.plot_figure()
            chartjsvariables = plot.get_ChartjsVariables()
            if result:
                imagename = result[0]
                content_file = result[1]
                image_item.image.save(imagename+'.png', content_file)
                image_item.save()           
        
        else:
        # The situation is that pic exists in db and web needs to create variables for chartjs
            plot = Plot(IPorCOM, start_datehour, total_hour)
            chartjsvariables = plot.get_ChartjsVariables()
        
                
    except T_H_Image.DoesNotExist:
        plot = Plot(IPorCOM, start_datehour, total_hour)
        result = plot.plot_figure()
        chartjsvariables = plot.get_ChartjsVariables()
        if result:
            imagename = result[0]
            content_file = result[1]
            image_item = T_H_Image()
            image_item.image_name = imagename
            image_item.image.save(imagename+'.png', content_file)
            image_item.save()
            
              
    context = {'IPorCOM':IPorCOM, 'img':image_item, 
               'start_datehour':start_datehour, 'chartjsvariables':chartjsvariables}
    return render(request, 'search/plot.html', context)

