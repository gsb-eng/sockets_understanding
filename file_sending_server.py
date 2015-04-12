from socket import *
import os


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
connectionSocket, address = serverSocket.accept()
path = connectionSocket.recv(1024)

print path + ' server pathhh received'

def write_file(path=None):
    if not path:
        path = connectionSocket.recv(1024)
    print(path) + '  --Here'
    if path.decode('utf-8')=="":
        raise TypeError('Should be of utf-8')
    fileName = os.path.basename(path).decode('utf-8')
    print fileName + '  At file decode'
    drive, tail = os.path.splitdrive( os.path.dirname(path) )
    directory = os.getcwd()+tail.decode('utf-8')
    if not os.path.exists(directory):
	os.makedirs(directory)

    file = open( directory +"/"+ fileName, 'wb' ) #open in binary
    data = connectionSocket.recv(1024)
    print data
    file.write(data)
    return data


if os.path.isfile(path):
    file = open(os.path.basename(path), 'wb' ) #open in binary
    data = connectionSocket.recv(1024)
    while (data):
        file.write(data)
        data = connectionSocket.recv(1024)
    file.close()


else:
    while True:
        try:
            data = write_file()
            while (data):
                data = connectionSocket.recv(1024)
                write_file(data)
            file.close()
        except TypeError, e:
            print str(e)
            break


connectionSocket.close()
print("connection closed")



