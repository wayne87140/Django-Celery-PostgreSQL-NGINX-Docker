from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

import json

from main.models import TaskResult
from main.utils.login_decorator import customed_login_required
from account.models import User

# Create your views here.
@customed_login_required
@never_cache
def main(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse('The password has already modified. Please reload page and re-login.')
    
    ## get disabled list
    if request.is_ajax():
        template_URL = 'main/content.html'
    else:
        template_URL = 'main/main.html'
    
    default_access = User.objects.get(username=current_user).Default_Access
    
    ## read device status from DB
    latest_result = TaskResult.objects.latest('pubDateTime')
    tablejson = latest_result.devices_with_tableHTML
    devicetable = json.loads(tablejson)  # the output is a dictionary {'IP_Port': 'table_html', ...} 
    
    htmlstring = ''
    if default_access == False:
        availablelist = json.loads(User.objects.get(username=current_user).AvailableList)
        for device in availablelist: ## sum up all html template
                htmlstring+=devicetable.get(device, '')        
        
    else:     
        disablelist = json.loads(User.objects.get(username=current_user).DisableList)        
        for device in devicetable: ## sum up all html template
            if device not in disablelist:
                htmlstring+=devicetable[device]
           
    context = {'tablestr':htmlstring}
    return render(request, template_URL, context)
    
