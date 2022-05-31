from __future__ import absolute_import, unicode_literals
from celery import shared_task

import time
import json
 
from main.utils import TCPIPcontact_server as TCP_server 
from main.utils.LabVIEW_ClusterArray import flatten
from main.utils.DataExtraction import Extraction
from main.utils.list_to_table import table_html
  
from main.models import TaskResult
   
@shared_task
def update_dev_sec():    
#   Request to have JSON string back.
    place_order = ['s', 's', '2ub', 's']
    cluster = ['', '', 5, 'F0']
    fl = flatten()
    sendMessage = fl.clustertobytes(cluster, place_order, concate=True)
#     receiveMessage = TCP_server.connect_server(sendMessage).decode('utf-8')
    receiveMessage = TCP_server.connect_server(sendMessage)

# transform original results to a dictionary and then to a json str
    

# save Type IPwithPort in connectinIP(dictionary) and IPandPort(list)    
    extract = Extraction()
    connectinIP = {}
    IPPort_table = {}
    IPandPort =[] #for searchbar
        
    rawdata = json.loads(receiveMessage)    
    for device in rawdata:        
        tablestr = table_html([device])
        
        if tablestr:
            IPwithPort =extract.IPwithPort(device['IP'], device['Port'])                  
            if device['Status']=='F':
                deviceType ='OFFLINE'
            else:
                deviceType = extract.device_type(device['Data'])       
                
            connectinIP[IPwithPort] = deviceType
            IPandPort.append(IPwithPort+'/'+deviceType)
            IPPort_table[IPwithPort] = tablestr 
    json_connectinIP = json.dumps(connectinIP)
    json_IPwithPort = json.dumps(IPandPort)
    json_IPPort_table = json.dumps(IPPort_table)
    

#   save to database
    TaskResult.objects.create(
        pubTime = str(int(time.time())),
        original_result = receiveMessage,
        devices_with_tableHTML = json_IPPort_table,
        connectinIP = json_connectinIP,
        IPPort = json_IPwithPort)

    return 'Success!!!'

@shared_task
def delete_dev_min():
    TaskResult.objects.all().delete()
    return 'Delete all results successfully !!!'




# if __name__ == '__main__':
#     update_dev_sec()