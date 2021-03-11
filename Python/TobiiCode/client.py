#//CLIENT// Tobii

import socket, subprocess, re, time, os

# receiving from server E-Prime
serverNameEP = '192.168.0.101'
serverPortEP = 5000
path = 'D:\\BlinksandBCITobii'
subdir = 'Tobii'
AllInstr = ''
print('AllInstr = ' + AllInstr)

if os.name == 'posix':
    sep = '/'
    python = 'python3'
elif os.name == 'nt':
    sep = '\\'
    python = 'python'

def receiveInstruction(AllInstr):
	print('AllInstr = ' + AllInstr)
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	    s.connect((serverNameEP, serverPortEP))
	    s.sendall(b'Ready')
	    data = s.recv(1024)
	print('Received', repr(data))
	received = data.decode('utf-8')
	nameFile = re.split('_',received)[0]
	nameDir = re.split('_',received)[1] 
	choicePath = re.split('_',received)[2]
	AllInstr = AllInstr + '##' + path+sep+nameDir+sep+subdir+sep+nameFile
	if choicePath=='Start':
		pathToCode = path+sep+'TobiiCode'+sep+'saveDocStart.py'
		print('pathToCode = '+pathToCode)
		print('Before trial begin')
	elif choicePath == 'End':
		pathToCode = path+sep+'TobiiCode'+sep+'saveDocEnd.py'
		print('At trial end')
	if len(received) != 0 :
	    print('Do something')
	    params = [python,pathToCode,nameFile,nameDir,path,subdir,AllInstr]
	    subprocess.call(params)
	return(AllInstr)

while True:
	print('Receiving instruction from E-Prime')
	AllInstr = receiveInstruction(AllInstr)
