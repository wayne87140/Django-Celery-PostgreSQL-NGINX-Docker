import imp
import time
import json
 
from SimDataExtraction import Extraction
from Simlist_to_table import table_html
from SimLabVIEW_ClusterArray import flatten

import SimTCPIPcontact_server as TCP_server 


def update_dev_sec():    
#   Request to have JSON string back.
    place_order = ['s', 's', '2ub', 's']
    cluster = ['', '', 5, 'F1']
    fl = flatten()
    sendMessage = fl.clustertobytes(cluster, place_order, concate=True)
#     receiveMessage = TCP_server.connect_server(sendMessage).decode('utf-8')
    receiveMessage = TCP_server.connect_server(sendMessage)

    # print(f'sendMSG is {sendMessage}')
    print(f'sendMSG is {sendMessage}, \nrecMSG is {receiveMessage}')

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

if __name__ == '__main__':
    update_dev_sec()
    