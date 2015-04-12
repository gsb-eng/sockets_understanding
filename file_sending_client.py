from socket import *
import fnmatch
import os


serverIP = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP,serverPort))
path = raw_input('Input Path:')


if os.path.exists(path):
    clientSocket.send(bytes(path))
    path_resp = clientSocket.recv(1024)


    if os.path.isfile(path):
        file = open(path, "rb")
        data = file.read(1024)
        while (data):
            clientSocket.send(data)
            data = file.read(1024)
        file.close()


    else:
        file_list = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.*'):
                file_list.append(os.path.join(root, filename).encode('utf-8'))
        print file_list
        file_list = iter(file_list)
        while True:
            file_transfer_done = False
            try:
                file_name = file_list.next()
            except StopIteration, e:
                str(e)
                break

            print('Sent file name to server %s' % file_name)
            clientSocket.send(file_name)
            file_resp = clientSocket.recv(1024)
            print('Received server response : %s' % file_resp)
            file = open(file_name, "rb")
            data = file.read(1024)
            while True:
                if data:
                    clientSocket.send(data)
                    print('Sent data to server')
                    data_resp = clientSocket.recv(1024)
                    print('Received server responce : %s' % data_resp)
                data = file.read(1024)
                if not data:
                    clientSocket.send('file_closed')
                    close_resp = clientSocket.recv(1024)
                    break
            file.close()
        clientSocket.send("close".encode('utf-8'))


else:
    print("Path is invalid!")

clientSocket.close()
print("connection closed")
