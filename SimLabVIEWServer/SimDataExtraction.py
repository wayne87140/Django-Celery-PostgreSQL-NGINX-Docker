class Extraction:
    '''
    The input is IP, Port, and string which has format like 
    "STX,1,0,A,TYPE,STATUS,TEST_PV,PRECOOL_PV,TEST_SV,PRECOOL_SV,PGM_NAME,CYCLE,STEP,HOUR,MIN,ERROR,END"
    This class extracts information form the string.
    Those information includes Type, PV, SV, and Error code.
    '''
    def __init__(self):
        self.TypeWithName = {'6':'THS', '13':'ATH', '3':'HAST', '7':'TSK',
                 '8':'TC', '83':'ATSK', '82':'TSC', '81':'ESS', '47':'NCO'}
        self.NamewithTypeNum = {'THS':'6', 'ATH':'13', 'HAST':'3', 'TSK':'7',
                 'TC':'8', 'ATSK':'83', 'TSC':'82', 'ESS':'81', 'NCO': '47', 'OFFLINE':'0'}        

    def IPwithPort(self, IP, Port)->str:
        if 'COM' in IP:
            return IP
        else:
            return IP+'_'+Port
    
    def device_type(self, Datastr)->str:
        STXlist = self.extract_str_list(Datastr)
        return self.TypeWithName[STXlist[4]]
   
    def createDeviceStatus(self, IP:str, Port:str, DataString:str)->dict:
        Datalist = self.extract_str_list(DataString)
        if len(Datalist)==1:
            return self.createOFFLINE(IP, Port)
        if Datalist[4] in ['6', '13', '3', '47']:
            return self.createTHS_ATH_HAST_NCO(IP, Port, Datalist)
        elif Datalist[4] in ['7', '8', '81']:
            return self.createTSK_TC_ESS(IP, Port, Datalist)
        elif Datalist[4] in ['82', '83']:
            return self.createATSK_TSC(IP, Port, Datalist)

        else:
            return None

    def extract_str_list(self, DataString:str)->list:
#         split string into list
        OutputList = DataString.split(',')
        return OutputList     

    def createOFFLINE(self, IP, Port)->dict:
        outdict = {}
        outdict['Type'] = 'OFFLINE'
        if 'COM' in IP:
            outdict['IP'] = IP
        else:
            outdict['IP'] = IP+'_'+Port
        return outdict 
            
    def createTHS_ATH_HAST_NCO(self, IP, Port, DataList:list)->dict:
        
        outdict = {}
        TypeName = self.TypeWithName.get(DataList[4])
        outdict['Type'] = TypeName
        if 'COM' in IP:
            outdict['IP'] = IP
        else:
            outdict['IP'] = IP+'_'+Port
            
        outdict['MachineOn'] = DataList[5]
        
  
        
        if TypeName == 'NCO':
            outdict['Temp PV'] = DataList[6]
            outdict['Temp SV'] = DataList[7]           
            outdict['Humi PV'] = '---.-'
            outdict['Humi SV'] = '---.-'           
        else:
            outdict['Temp PV'] = DataList[6]
            outdict['Humi PV'] = DataList[7]
            outdict['Temp SV'] = DataList[8]
            outdict['Humi SV'] = DataList[9]
        
        if TypeName == 'NCO':
            outdict['Error']=DataList[11]
        elif TypeName == 'HAST':
            outdict['Error']=DataList[14]         
        else:
            outdict['Error']=DataList[15]
            
        return outdict
        
    def createTSK_TC_ESS(self, IP, Port, DataList:list)->dict:
        outdict = {}
        TypeName = self.TypeWithName.get(DataList[4])
        outdict['Type'] = TypeName
        
        if 'COM' in IP:
            outdict['IP'] = IP
        else:
            outdict['IP'] = IP+'_'+Port
            
        outdict['MachineOn'] = DataList[5]  
                  
        if TypeName == 'ESS':
            outdict['Temp PV'] = DataList[6]
            outdict['Humi PV'] = DataList[7]
            outdict['Temp SV'] = DataList[9]
            outdict['Humi SV'] = DataList[10]            
        else:
            outdict['Test PV'] = DataList[6]
            outdict['Preheat PV'] = DataList[7]
            outdict['Test SV'] = DataList[9]
            outdict['Preheat SV'] = DataList[10]
            
        outdict['Precool PV'] = DataList[8]
        outdict['Precool SV'] = DataList[11]        
        outdict['Error']=DataList[17]
        return outdict
    
    def createATSK_TSC(self, IP, Port, DataList:list)->dict:
        outdict = {}
        TypeName = self.TypeWithName.get(DataList[4])
        outdict['Type'] = TypeName
        if 'COM' in IP:
            outdict['IP'] = IP
        else:
            outdict['IP'] = IP+'_'+Port
            
        outdict['MachineOn'] = DataList[5]
        outdict['Test PV'] = DataList[6]
        outdict['Precool PV'] = DataList[7]
        outdict['Test SV'] = DataList[8]           
        outdict['Precool SV'] = DataList[9] 
        outdict['Error']=DataList[15]
        return outdict
    