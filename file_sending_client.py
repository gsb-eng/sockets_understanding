from socket import *
import fnmatch
import os


serverIP = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP,serverPort))
path = raw_input('Input Path:')
print path

if os.path.exists(path):
    clientSocket.send(bytes(path))


    if os.path.isfile(path):
        file = open(path, "rb")
        data = file.read(1024)
        while (data):
            clientSocket.send(data)
            data = file.read(1024)
        file.close()


    else:
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.*'):
                server_response = clientSocket.recv(1024)
                if server_response == "clear":
                    print( os.path.join(root, filename).encode('utf-8') )
                    clientSocket.send(os.path.join(root, filename).encode('utf-8'))
                    file = open(root+"/"+filename, "rb")
                    data = file.read(1024)
                    while (data):
                        clientSocket.send(data)
                        data = file.read(1024)
                    file.close()
        clientSocket.send("close".encode('utf-8'))


else:
    print("Path is invalid!")

clientSocket.close()
print("connection closed")
