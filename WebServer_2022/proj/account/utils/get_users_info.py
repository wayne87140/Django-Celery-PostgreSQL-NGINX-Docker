import json

from main.utils import TCPIPcontact_server as TI_server 
from main.utils.LabVIEW_ClusterArray import flatten

def get_users_info():
    place_order = ['s', 's', '2ub', 's']
    cluster = ['', '', 5, 'F1']
    fl = flatten()
    sendMessage = fl.clustertobytes(cluster, place_order, concate=True)
    receiveMessage = TI_server.connect_server(sendMessage)
    UserListofDict = json.loads(receiveMessage)
    
    return UserListofDict