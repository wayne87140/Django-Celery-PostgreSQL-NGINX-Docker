def splitIP(IPandCOM:dict):
    allIP = {k:v for k,v in IPandCOM.items() if 'COM' not in k}
    allCOM = {k:v for k,v in IPandCOM.items() if 'COM' in k}
    return (allIP, allCOM)

def sortIP_keyFunction(eachIP:tuple):
    returnval = (eachIP[0].split('.')[0],
                 eachIP[0].split('.')[1],
                 eachIP[0].split('.')[2],
                 eachIP[0].split('.')[3].split('_')[0],
                 eachIP[0].split('_')[1]
    )                 
    return returnval
    
def sortIP(allIP):
    sortedIP = {k:v for k, v in sorted(allIP.items(), key=sortIP_keyFunction)}
    return sortedIP
                                       
def sortCOM_keyFunction(eachCOM:tuple):
    returnval = (eachCOM[0].split('COM')[1].split('_')[0],
                 eachCOM[0].split('COM')[1].split('_')[1]
    )                 
    return returnval

def sortCOM(allCOM):
    sortedCOM = {k:v for k, v in sorted(allCOM.items(), key=sortCOM_keyFunction)}
    return sortedCOM

def createInputLabel(IPCOM, checked=''):
    if checked=='checked':
        displaytext = IPCOM[1][0]
    else:
        displaytext = IPCOM[1]
    insertstr = f'''
  <p>
    <input type="checkbox" id={IPCOM[0]} name={IPCOM[0]} {checked}>
    <label for={IPCOM[0]} >{IPCOM[0]}/{displaytext}</label><br> 
  </p>   
    '''

    return insertstr
    
def IPCOMform(connectinIP:dict, favoriteIP:dict, disabled:list):
    for device in disabled:
        connectinIP.pop(device, None)
        
    allIPCOM = {**connectinIP, **favoriteIP}
    ## use {**dict1, **dict2} or dict2.update(dict1) to merge to dict
    
    htmlform = ''
    (allIP, allCOM) = splitIP(allIPCOM)
    sortedIP = sortIP(allIP)
    sortedCOM = sortCOM(allCOM)
    totalPCOM = {**sortedIP, **sortedCOM}

    for IPCOM in totalPCOM.items():
        if type(IPCOM[1])==tuple:           
            htmlform+=createInputLabel(IPCOM, checked='checked')
        else:
            htmlform+=createInputLabel(IPCOM)        
    return htmlform


# if __name__=='__main__':
#     conn = {'127.1.0.1_15':'ths', '127.0.1.1_2':'ads', 'COM5_2':'sew', 'COM1_2':'sesw',
#             '127.0.0.1_1':'sss', '124.0.0.1_5':'ths', '121.0.0.1_15':'ths'}
#      
#     favr = {'127.1.0.1_15':('ths',), '127.0.2.1_2':('sads',), 'COM4_2':('s4ew',), 'COM1_2':('sesw',),
#             '127.0.0.1_2':('swss',), '122.0.0.1_15':('tshs',), '120.0.0.1_15':('tashs',)}   
#      
#     print(IPCOMform(conn, favr))
    

#     htmlform = '''
#     <form method="post" action="{% url 'favorite:settings}">
#         <input type='hidden' name='csrfmiddlewaretoken' value='{{ csrf_token }}' />
#         {% csrf_token %}
#     '''
#     htmlform+='<input type="submit" value="送出"></form>'     