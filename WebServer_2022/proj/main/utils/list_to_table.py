from main.utils.DataExtraction import Extraction


def table_html(processed_list:list, disablelist=[])->str:
    outstr = ''
    
    extract = Extraction()
    
    Machinestatus = {'0':'STOP', '1':'Run', '2':'Scheduled', '3':'Standby', '4':'Defrost', '5':'Pause'}
    
    for subdict in processed_list:

        DataDict = extract.createDeviceStatus(subdict['IP'], subdict['Port'], subdict['Data'])
        
        if DataDict:
            if DataDict['IP'] not in disablelist:
                
                # subdict['Data'] is a string with data format like :"STX,1, ..."
                if subdict['Status']=='F':                       # device status is 'offline'
                    outstr += table_offline(DataDict, subdict['IP'])
        
                elif DataDict['Error']!='0':                       # device has error
                    outstr += table_status(DataDict, subdict['IP'])
                    
                elif DataDict['MachineOn']!='1':                     # device has another status
                    status = Machinestatus[DataDict['MachineOn']]
                    outstr += table_status(DataDict, subdict['IP'],status)
        
                elif DataDict['Type'] in ['THS', 'ATH', 'HAST', 'ATSK', 'TSC', 'ESS', 'NCO']:
                # with 2 pieces of data which are Temp and Humi
                    outstr += table_temp_humi(DataDict, subdict['IP'])
        
                elif DataDict['Type'] in ['TSK', 'TC']:
                # with 3 pieces of data which are test, preheat, and precool
                    outstr += table_temp_preheat_cool(DataDict, subdict['IP'])
                

    return outstr


def table_offline(DataDict: dict, justIP:str) -> str:
    
    outstr = \
f'''
<a href="../search/plot/{justIP}/">
<table>
<tr>
    <td class='ad2'>{DataDict['Type']}</td>    <!-- Device Name -->
    <td class='ad3'>{DataDict['IP']}</td>      <!-- IP with Port-->
</tr>
<tr class='offline'>
    <td colspan='3' rowspan='4' class='offlinetd'>Offline</td>
</tr>
<tr>
</tr>
<tr>
</tr>
<tr>
</tr>    
</table>
</a>
'''
    return outstr


def table_status(DataDict: dict,justIP:str, status='error') -> str:
    if DataDict['Type'] in ['THS', 'ATH', 'ESS', 'HAST', 'NCO']:
        text = 'Temp'
        b_color = 'red'
    else:
        text = 'Test'
        b_color = 'green'
    
#   DataDict['Error'] = W12(Warn12) or L5(Limit12) or E35(Error12)
    L_W_E_judge = DataDict['Error'][0]
    ErrorCode = DataDict['Error'][1:]
    
    if L_W_E_judge=='L':      # Limit
        errortext = 'Limit('+ ErrorCode +')'
        class_c_tr='c_limittr'       
    
    elif L_W_E_judge=='W':      # Warn
        errortext = 'Warn('+ ErrorCode +')'
        class_c_tr='c_warntr'        

    elif L_W_E_judge=='E':      # Error
        errortext = 'Error('+ ErrorCode +')'
        class_c_tr='c_errortr'       
        
    else:
        errortext = status
        class_c_tr='c_stoptr'        
        
#     if status=='error':   
#         errortext = 'ERROR('+ DataDict['Error'] +')'
#         class_c_tr='c_errortr'
#     else:
#         errortext = status
#         class_c_tr='c_stoptr'    
    outstr = \
f'''
<a href="../search/plot/{justIP}/">
<table>
<tr>
    <td class='ad2'>{DataDict['Type']}</td>    <!-- Device Name -->
    <td class='ad3'>{DataDict['IP']}</td>      <!-- IP with Port-->
</tr>
<tr class='b1'>
    <td class='bd1_{b_color}'>{text}</td>
    <td rowspan='3' colspan='2' class='bd4_{b_color}'>{DataDict[text+' PV']} &#8451 </td>    <!-- PV of Temp -->
</tr>
<tr class='b2'>
    <td>SV</td>
</tr>
<tr class='b3'>
    <td class='bd3_{b_color}'>{DataDict[text+' SV']}</td>        <!-- SV of Temp -->
</tr>
<tr class={class_c_tr}>
    <td colspan='3' class='c_stoptd'>{errortext}</td>
</tr>    
</table>
</a>
'''
    return outstr


def table_temp_humi(DataDict: dict, justIP:str) -> str:
    if DataDict['Type']=='ATSK' or  DataDict['Type']=='TSC':
        text = ['Test', 'Precool']
        b_color ='green'
        TorH = '&#8451'
    else:
        text = ['Temp', 'Humi']
        TorH = '%'
        b_color = 'red'
    outstr = \
f'''
<a href="../search/plot/{justIP}/">
<table>
<tr>
    <td class='ad2'>{DataDict['Type']}</td>    <!-- Device Name -->
    <td class='ad3'>{DataDict['IP']}</td>      <!-- IP with Port-->
</tr>
<tr class='b1'>
    <td class='bd1_{b_color}'>{text[0]}</td>
    <td rowspan='3' colspan='2' class='bd4_{b_color}'>{DataDict[text[0]+' PV']} &#8451 </td>    <!-- PV of Temp -->
</tr>
<tr class='b2'>
    <td>SV</td>
</tr>
<tr class='b3'>
    <td class='bd3_{b_color}'>{DataDict[text[0]+' SV']}</td>        <!-- SV of Temp -->
</tr>
<tr class='c1'>
    <td class='cd1_blue'>{text[1]}</td>
    <td rowspan='3' colspan='2' class='cd4_blue'>{DataDict[text[1]+' PV']}{TorH}</td>           <!-- PV of Humi -->
</tr>
<tr class='c2'>
    <td>SV</td>
</tr>
<tr class='c3'>
    <td class='cd3_blue'>{DataDict[text[1]+' SV']}</td>        <!-- SV of Humi -->
</tr>
</table>
</a>
'''
    return outstr


def table_temp_preheat_cool(DataDict: dict, justIP:str) -> str:
    outstr = \
f'''
<a href="../search/plot/{justIP}/">
<table>
<tr>
    <td colspan='2' class='ad2'>{DataDict['Type']}</td>    <!-- Device Name -->
    <td colspan='4' class='ad3'>{DataDict['IP']}</td>      <!-- IP with Port-->
</tr>
<tr class='b1'>
    <td colspan='2' class='bd1_green'>Test</td>
    <td rowspan='3' colspan='4' class='bd4_green'>{DataDict['Test PV']} &#8451 </td>    <!-- PV of Temp -->
</tr>
<tr class='b2'>
    <td colspan='2'>SV</td>
</tr>
<tr class='b3'>
    <td colspan='2' class='bd3_green'>{DataDict['Test SV']}</td>        <!-- SV of Temp -->
</tr>
<tr class='c1'>
    <td class='cd1_red'>Preheat</td>
    <td rowspan='3' colspan='2' class='cd4border_red'>{DataDict['Preheat PV']} &#8451 </td>  <!-- PV of Preheat -->
    <td class='cd5'>Precool</td>
    <td rowspan='3' colspan='2' class='cd8'>{DataDict['Precool PV']} &#8451 </td>        <!-- PV of PreCool -->
</tr>
<tr class='c2'>
    <td class='cd2'>SV</td>
    <td class='cd6'>SV</td>
</tr>
<tr class='c3'>
    <td class='cd3_red'>{DataDict['Preheat SV']}</td>       <!-- SV of Preheat -->
    <td class='cd7'>{DataDict['Precool SV']}</td>       <!-- SV of Precool -->
</tr>
</table>
</a>
'''
    return outstr