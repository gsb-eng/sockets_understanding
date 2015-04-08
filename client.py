import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
    message = raw_input('Please enter the message: ')
    s.send(message)
    data = s.recv(BUFFER_SIZE)
    if data == 'con_close':
        s.close()
        break
    print "received data: ", data
