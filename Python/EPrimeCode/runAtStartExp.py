# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 17:00:25 2018

@author: QinXinlan
"""

#//SERVER// E-Prime

import socket, datetime, time, os

if os.name == 'posix':
    sep = '/'
    python = 'python3' 
elif os.name == 'nt':
    sep = '\\'
    python = 'python'

serverNameP = '192.168.0.133'
serverPortP = 6002
serverNameT = '192.168.0.180'
serverPortT = 5001

    
def sendInstruction():
    # E-Prime as master
    serverNameEP = '192.168.0.101'
    serverPortEP = 5000
    # Getting today's date for name folder
    today = datetime.date.today()
    todaystr = today.isoformat()
    # initalizaing instruction
    instruction = ''
    AllInstr = ''
    # number of computer client connected to E-Prime
    nbOrdiConnect = 2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind socket to local host and port
        s.bind((serverNameEP, serverPortEP))
        # Start listening on socket
        s.listen(10)
        # Looping for several instructions
        while True:
            print('while')
            # Giving instruction
            if len(instruction)==0:
                instruction = input('Write instructions (name of file or copy) -> ')
                if instruction == 'copy':
                    endIns = '_End'
                else:
                    endIns = '_Start'
                instruction = instruction + '_' + todaystr + endIns
                print(instruction)
            # Looping to talk to each client for one instruction
            for connect in range(0,nbOrdiConnect):
                print('connect = ' + str(connect+1))
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data: break
                        print('Received', repr(data))
                        conn.sendall(instruction.encode('utf-8'))
            # If we are at the end of the trial, we check whether Tobii and Phantom have no recording problems
            if endIns == '_End':
                print('Receiving feedback from Tobii')
                messageT = ''
                while len(messageT) == 0 :
                    # print('Receving instruction from Tobii')
                    messageT = receiveInstructionT()
                    print('message Tobii = ' + messageT)
                print('Receiving feedback from Phantom')
                messageP = ''
                while len(messageP) == 0 :
                    # print('Receving instruction from Phantom')
                    messageP = receiveInstructionP()
                    print('message Phantom = ' + messageP)
            AllInstr = AllInstr + '##' + instruction
            # re initializing instruction
            instruction = ''
            print('instruction = ' + instruction)
            print('AllInstr = ' + AllInstr)
        s.close()
    time.sleep(5)

def receiveInstructionP():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        connected = False
        print('Trying to connect')
        while not connected:
            try:
                print('Trying')
                s.connect((serverNameP, serverPortP))
                connected = True
                print('Connected')
            except Exception as e:
                print('Except')
                pass # Do nothing just try again
        s.sendall(b'Ready')
        data = s.recv(1024)
        s.close()
   # print('Received', repr(data))
    received = data.decode('utf-8')
    return(received)

def receiveInstructionT():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        connected = False
        while not connected:
            try:
                s.connect((serverNameT, serverPortT))
                connected = True
            except Exception as e:
                pass # Do nothing just try again
        s.sendall(b'Ready')
        data = s.recv(1024)
        s.close()
   # print('Received', repr(data))
    received = data.decode('utf-8')
    return(received)

sendInstruction()
