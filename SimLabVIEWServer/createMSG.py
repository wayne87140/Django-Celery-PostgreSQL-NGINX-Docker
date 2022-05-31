import random


def device_status():
    randT = 50*random.random()
    randRH =100*random.random()
    orgMSG = r'[{"Status":"T","IP":"127.0.0.1","Port":"4001","Data":"STX,1,0,A,6,1,%.2f,%.2f,25.00,65.0,kson.pgm,1,2,0,29,0,END","Tag(UCS2LE)":"1\u00002\u00007\u0000.\u00000\u0000.\u00000\u0000.\u00001\u0000","Description(UCS2LE)":"","Model":"","Serial":""}]' %(randT, randRH)
    sendMSG = len(orgMSG).to_bytes(4, byteorder='big')+bytes(orgMSG,encoding='ascii')
    return sendMSG

def user_info():
    userMSG = '[{"User Name":"aaaa","Password":"aaaa","Default Access":"Full Control",\
"Description(UCS2LE)":"","Disable list":"","Read Only list":"","Normal list":"",\
"Full Control list":"127.0.0.1_4008,127.0.0.1_4007,127.0.0.1_4006,127.0.0.1_4005,\
127.0.0.1_4004,127.0.0.1_4003,127.0.0.1_4002,127.0.0.1_4001,"},\
{"User Name":"bbbb","Password":"bbbb","Default Access":"Full Control",\
"Description(UCS2LE)":"","Disable list":"","Read Only list":"","Normal list":"","Full Control list":""}]'
    sendMSG = len(userMSG).to_bytes(4, byteorder='big')+bytes(userMSG, encoding='ascii')
    return sendMSG


if __name__ == '__main__':
    print(user_info(), sep='/n')