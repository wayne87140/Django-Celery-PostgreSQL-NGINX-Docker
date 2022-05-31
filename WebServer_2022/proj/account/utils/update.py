import json
 
from account.utils.get_users_info import get_users_info
from account.models import User


def update_individual_user_info(input_username):
    usersListofDict = get_users_info()
    for each_user in usersListofDict:
        if each_user.get('User Name')==input_username:
            jsonDisablelist = json.dumps(each_user['Disable list'].rstrip(',').split(','))        
            available = (each_user['Read Only list']+
                        each_user['Normal list']+
                        each_user['Full Control list'])

            available = sorted(available.rstrip(',').split(','))
            jsonAvailablelist = json.dumps(available)
            
            if each_user['Default Access']=='Disable':
                defaultAccessDisable = False
            else: 
                defaultAccessDisable = True
    
            try:
                user = User.objects.get(username = each_user['User Name'])
            except User.DoesNotExist:
                user = None
    
            if user==None:
                user = User()
                user.username = each_user['User Name']
                user.set_password(each_user['Password'])
                user.DisableList = jsonDisablelist
                user.AvailableList = jsonAvailablelist
                user.Default_Access = defaultAccessDisable
                user.save()
                
            else:
                raw_password = each_user['Password']
                if not user.check_password(raw_password):
                    user.set_password(raw_password)
                user.DisableList = jsonDisablelist
                user.AvailableList = jsonAvailablelist
                user.Default_Access = defaultAccessDisable
                user.save()
            
            return "OK"
    return None
