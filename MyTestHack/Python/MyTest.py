import time, threading, sys, socket, subprocess
from Functions import recv_timeout, Result

Log = open('logs.txt','wb',0)
WithClient = None
WithServer = None
host = None
port = None
Thread = None
errors = 0
numberQuestion = 0

def MyTestOpen():
    with subprocess.Popen(['MyTestStudent.exe']) as proc:
        while proc.poll()== None:
            time.sleep(2)
            continue
    quit()
def Connection():
    try:
        global WithClient, WithServer, Thread
        sock = socket.socket()
        sock.bind(('', 6666))
        sock.listen(1)
        print('Waiting for connection from client')
        if(not Thread):
            Thread = threading.Thread(target=MyTestOpen)
            Thread.start()
        WithClient, ClientAddr = sock.accept()
        print('Client : {0} connected!'.format(ClientAddr))
        WithServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print('Waiting for connection to server')
        WithServer.connect((host,port))
        print('To sever connected')
    except socket.error as e:
        print("Can't connection:\n"+str(e))
        
def ConnectionWithoutPrints():
    try:
        global WithClient, WithServer, Thread
        sock = socket.socket()
        sock.bind(('', 6666))
        sock.listen(1)
        if(not Thread):
            Thread = threading.Thread(target=MyTestOpen)
            Thread.start()
        WithClient, ClientAddr = sock.accept()
        WithServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        WithServer.connect((host,port))
    except socket.error as e:
        print("Can't connection:\n"+str(e)+"\nTrying again...")
        time.sleep(2)
        ConnectionWithounPrints()
        
def Communication():
    global WithClient,WithServer, numberQuestion
    FixErrors = errors
    while True:
        try:
            data = recv_timeout(WithClient,0.5)
            if b'{' in data and b'}' in data and b'INFOPROCESS' in data:
                temp=list(data[data.find(b'}')+1:])
                if temp[-8] == 2 and FixErrors>0:
                    FixErrors-=1
                else:
                    numberQuestion += 1
                    temp[6] = numberQuestion
                    temp[10] = errors-FixErrors
                    temp[-8] = 4
                    temp = bytes(temp)
                    data=data[:data.find(b'}')+1]+temp
            if b'RESULT' in data:
                temp=list(data[data.rfind(b'}')+1:])
                count = temp[14]
                temp[22] = count-errors
                temp[18] = count
                temp[26] = errors
                temp[30] = 0
                temp[-13], temp[-12], temp[-11] = Result(temp[38]-errors)
                temp[2] = 5
                temp = bytes(temp)
                data=data[:data.rfind(b'}')+1]+temp
                temp = list(data[data.find(b'}')+5:data.rfind(b'{')-1])
                kol = 0
                FixErrors = errors
                for i in range(len(temp)-1):
                    if temp[i] == 1 and temp[i+1] == 2:
                        if FixErrors > 0:
                            FixErrors -=1
                            continue
                        temp[i+1] = 4
                        kol+=1
                    if kol == count:
                        break
                temp = bytes(temp)
                data = data[:data.find(b'}')+5] + temp +data[data.rfind(b'{')-1:]
                Log.write(b'FromClient:\n'+data+b'\n\n')
                WithServer.send(data)
                return
            if data:
                Log.write(b'FromClient:\n'+data+b'\n\n')
                WithServer.send(data)
                if b'QUIT\r\n' in data:
                    ConnectionWithoutPrints()
                    continue
            data = recv_timeout(WithServer,0.5)
            if data:
                Log.write(b'FromServer:\n'+data+b'\n\n')
                WithClient.send(data)
        except socket.error as e:
            print('Error: \n' +str(e))
            WithServer.close()
            WithClient.close()

def StartProgram(h,p,err):
    global host, port, numberQuestion, errors
    errors = err
    numberQuestion = 0
    host,port = h,p
    Connection()
    Communication()
    print('Waiting for close the application...')
    Thread.join()

#StartProgram('127.0.0.1',5005)
