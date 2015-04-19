import datetime
import socket
import threading


host = ''
port = 2628
connectionSevered = 0


class client(threading.Thread):

    def __init__(self, conn):
        super(client, self).__init__()
        self.conn = conn
        self.data = ""

    def run(self):
        while True:
            self.data += self.conn.recv(1024)
            if self.data.endswith(u"\n"):
                print str(datetime.datetime.now()) + ':' + \
                    str(self.data).replace("\n", "")
                self.data = ""

    def send_msg(self, msg):
        self.conn.send(msg)

    def close(self):
        self.conn.close()


class ConAccept(threading.Thread):
    clients = {}

    def __init__(self, con):
        super(ConAccept, self.__init__())
        self.con = con

    def run(self):
        while True:
            client, address = self.con.accept()
            if client:
                self.clients[client] = client
                print self.clients

    def start_client(self, con):
        c = client(con)
        c.daemon = True
        c.start()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
except socket.error, e:
    import sys
    print 'Failed to create socket'
    print str(e)
    sys.exit()

con_thread = ConAccept(s)
conn, address = s.accept()
c = client(conn)
c.daemon = True
c.start()
print '[+] Client connected: {0}'.format(address[0])
c.send_msg(u"How are you? \n")
print "connectionSevered:{0}".format(connectionSevered)
while (connectionSevered == 0):
    try:
        response = raw_input()
        c.send_msg(response + u"\n")
    except:
        c.close()
