import datetime
import socket
import threading


TCP_IP = '23.229.145.162'
TCP_PORT = 3306
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


class client(threading.Thread):
    def __init__(self, con):
        super(client, self).__init__()
        self.con = con
        self.data = ""

    def run(self):
        while True:
            self.data += self.con.recv(1024)
            if self.data.endswith("\n"):
                print str(datetime.datetime.now()) + ':' + \
                    str(self.data).replace("\n", "")
                self.data = ""

    def send_msg(self, msg):
        self.con.send(msg)

    def con_close(self):
        self.con.close()

c = client(s)
c.deamon = True
c.start()

while True:
    try:
        message = raw_input()
        c.send_msg(message)
    except:
        c.con_close()
