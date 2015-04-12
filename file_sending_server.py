from socket import *
import os


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
connectionSocket, address = serverSocket.accept()
path = connectionSocket.recv(1024)

connectionSocket.send('path_received')

if os.path.isfile(path):
    file = open(os.path.basename(path), 'wb' ) #open in binary
    data = connectionSocket.recv(1024)
    while (data):
        file.write(data)
        data = connectionSocket.recv(1024)
    file.close()


else:
    while True:
        path = connectionSocket.recv(1024)
        print('Received file from client: %s' % path)
        connectionSocket.send('file_path_received')
        print('Sent responce to client : %s' % ('file_path_received'))
        print(path)
        if path.decode('utf-8')=="":
            break
        fileName = os.path.basename(path)
        print('File name received : %s' % fileName)
        drive, tail = os.path.splitdrive( os.path.dirname(path) )
        directory = os.getcwd()+tail
        print directory
        if not os.path.exists(directory):
            os.makedirs(directory)

        file = open( directory +"/"+ fileName, 'wb' ) #open in binary
        print('New file created : %s' % fileName)
        data = connectionSocket.recv(1024)

        while True:
            file.write(data)
            print('File write done')
            connectionSocket.send('Processed')
            data = connectionSocket.recv(1024)
            if 'file_closed' in data:
                connectionSocket.send('file_done')
                break
        file.close()


connectionSocket.close()
print("connection closed")
