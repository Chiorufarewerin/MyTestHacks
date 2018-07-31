import time,socket

def recv_timeout(the_socket,timeout=2): # Get all data
    #make socket non blocking
    the_socket.setblocking(0)
     
    #total data partwise in an array
    total_data=[]
    data=b''
     
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
         
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
    toReturn=b''
    for i in total_data:
        toReturn+=i
    return toReturn

def GetNumber(Numbers,Questions,Start):
    Questions-=1
    some = Start
    while some<16:
        if Questions == 0:
            Numbers.append(some)
            return
        some+=Start
        Questions-=1
    Numbers.append(some)
    if Questions == 0:
        return
    GetNumber(Numbers,Questions,Start/2)

def GetNumberFromFloat(koef,num):
    newkoef=1
    for i in range(koef):
        newkoef/=2
    return 16*newkoef*num/newkoef
        
def Result(Questions):
    if Questions == 0:
        return (0,0,0)
    if Questions == 1:
        return (0,int('0xf0',base=16),63)
    if Questions == 2:
        return (0,0,64)
    if Questions == 3:
        return (0,8,64)
    Numbers = list()
    GetNumber(Numbers,Questions-2,8)
    first=0; second=0; third=0
    for Number in Numbers:
        if Number == 16:
            first+=1
            continue
        if Number.is_integer():
            second = Number
        else:
            second = int(Number)
            third = GetNumberFromFloat(first - 3,Number - int(Number))
    return (int(hex(int(third))+'0',base=16),int(hex(int(first))+hex(int(second))[2:],base=16),64)
    
