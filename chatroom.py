import socket
import threading
import random

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    nicknames = ['Anonymous']

    def __init__(self, port, mw):
        self.mw = mw
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(1)
        self.mw.messageRecieved('Server started on port ' + str(port) + '.')
        self.sThread = threading.Thread(target=self.run)
        self.sThread.daemon = True
        self.sThread.start()

    def handler(self, c, a):
        while True:
            nick = 'Anonymous_' + str(random.randint(1, 999))
            if nick in self.nicknames:
                pass
            else:
                self.nicknames.append(nick)
                break
        c.send(bytes('Connected', 'utf-8'))
        while True:
            try:
                data = c.recv(1024)
            except:
                print(str(a[0]) + ':' + str(a[1]) + ' disconnected.')
                self.connections.remove(c)
                self.nicknames.remove(nick)
                c.close()
                break
            if str(data, 'utf-8').startswith('_delnick'):
                while True:
                    nick = 'Anonymous_' + str(random.randint(1, 999))
                    if nick in self.nicknames:
                        pass
                    else:
                        self.nicknames.append(nick)
                        break
            elif str(data, 'utf-8').startswith('_nick'):
                pnick = str(data, 'utf-8').split()[1]
                if pnick in self.nicknames:
                    c.send(bytes('Nickname unavailable or in use. Please try again.', 'utf-8'))
                else:
                    self.nicknames.remove(nick)
                    nick = pnick
                    self.nicknames.append(nick)
                    c.send(bytes('Nickname set to ' + nick + '.', 'utf-8'))
            else:
                for connection in self.connections:
                    connection.send(bytes(nick + ': ' + str(data, 'utf-8'), 'utf-8'))

    def run(self):
        while True:
            c, a = self.sock.accept()
            self.cThread = threading.Thread(target=self.handler, args=(c,a))
            self.cThread.daemon = True
            self.cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]) + ' connected.')

    def announce(self, msg):
        for connection in self.connections:
            connection.send(bytes(msg, 'utf-8'))

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self, msg):
        self.sock.send(bytes(msg, 'utf-8'))

    def __init__(self, address, port, mw):
        self.mw = mw
        try:
            self.sock.connect((address, int(port)))
        except:
            self.mw.messageRecieved('Unable to connect to server.')
            return

        self.mw.fileButton.Enable(1, False)
        self.mw.fileButton.Enable(2, False)
        self.mw.editButton.Enable(3, True)
        self.mw.inputButton.Enable()
        self.rThread = threading.Thread(target=self.reciever)
        self.rThread.daemon = True
        self.rThread.start()

    def reciever(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            self.mw.messageRecieved(str(data, 'utf-8'))
