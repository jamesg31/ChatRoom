import socket
import threading

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    port = 9000

    def __init__(self):
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(1)
        hThread = threading

    def handler(self, c, a):
        nick = 'Anonymous'
        c.send(bytes('Connected', 'utf-8'))
        while True:
            try:
                data = c.recv(1024)
            except:
                print(str(a[0]) + ':' + str(a[1]) + ' disconnected.')
                self.connections.remove(c)
                c.close()
                break
            if str(data, 'utf-8').startswith('_nick'):
                nick = str(data, 'utf-8').split()[1]
            else:
                for connection in self.connections:
                    print(nick + ': ' + str(data, 'utf-8'))
                    connection.send(bytes(nick + ': ' + str(data, 'utf-8'), 'utf-8'))

    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]) + ' connected.')

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self, msg):
        self.sock.send(bytes(msg, 'utf-8'))

    def __init__(self, address, port, mw):
        self.mw = mw
        self.sock.connect((address, port))

        rThread = threading.Thread(target=self.reciever)
        rThread.daemon = True
        rThread.start()

    def reciever(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            self.mw.MessageRecieved(str(data, 'utf-8'))
