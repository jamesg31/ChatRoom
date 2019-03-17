import wx
from chatroom import Client, Server

class mainWindow(wx.Frame):
    def __init__(self):
        super(mainWindow, self).__init__(parent=None, title='Chat Room', size=(250,350), style = wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION)

        panel = wx.Panel(self)
        menuBar = wx.MenuBar()
        self.fileButton = wx.Menu()
        self.editButton = wx.Menu()

        connectItem = self.fileButton.Append(1, 'Connect')
        hostItem = self.fileButton.Append(2, 'Host')
        exitItem = self.fileButton.Append(wx.ID_EXIT, 'Exit')
        menuBar.Append(self.fileButton, 'File')

        addNickname = self.editButton.Append(3, 'Set Nickname')
        remNickname = self.editButton.Append(4, 'Remove Nickname')
        menuBar.Append(self.editButton, 'Edit')

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.connectMenu, connectItem)
        self.Bind(wx.EVT_MENU, self.host, hostItem)
        self.Bind(wx.EVT_MENU, self.quit, exitItem)
        self.Bind(wx.EVT_MENU, self.setNickname, addNickname)
        self.Bind(wx.EVT_MENU, self.delNickname, remNickname)

        self.editButton.Enable(3, False)
        self.editButton.Enable(4, False)

        self.chatText = wx.TextCtrl(panel, pos=(10,10), size=(215,235), style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.inputText = wx.TextCtrl(panel, pos=(10,255), size=(150,25))
        self.inputButton = wx.Button(panel, pos=(170,255), size=(55,25), label = 'Send')
        self.chatText.Bind(wx.EVT_SET_FOCUS, self.focus)
        self.inputButton.Bind(wx.EVT_BUTTON, self.sendPressed)
        self.inputButton.Disable()
        self.Show(True)

    def quit(self, e):
        self.Close()

    def focus(self, e):
        return True

    def sendPressed(self, e):
        msg = self.inputText.GetValue()
        self.client.sendMsg(msg)
        self.inputText.SetValue('')

    def connectMenu(self, e):
        connectWindow(self)

    def host(self, e):
        hostWindow(self)

    def connectClient(self, address, port):
        self.chatText.write('Connecting to server...\n')
        self.client = Client(address, port, self)

    def messageRecieved(self, message):
        self.chatText.write(message + '\n')

    def setNickname(self, e):
        nicknameWindow(self)
        self.editButton.Enable(4, True)

    def delNickname(self, e):
        self.client.sendMsg('_delnick')
        self.chatText.write('Nickname Removed.\n')
        self.editButton.Enable(4, False)

class connectWindow(wx.Frame):
    def __init__(self, mw):
        self.mw = mw;
        super(connectWindow, self).__init__(parent=None, title='Connect', size=(250,150), style = wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION)

        panel = wx.Panel(self)

        wx.StaticText(panel, pos=(10,11), label='Hostname:')
        wx.StaticText(panel, pos=(43,42), label='Port:')
        self.hostText = wx.TextCtrl(panel, pos=(75,10), size=(150,20))
        self.portText = wx.TextCtrl(panel, pos=(75,40), size=(150,20))
        connectButton = wx.Button(panel, pos=(30,70), size=(170,25), label = 'Connect')

        connectButton.Bind(wx.EVT_BUTTON, self.connectPressed)
        self.Show(True)

    def connectPressed(self, e):
        self.mw.connectClient(self.hostText.GetValue(), self.portText.GetValue())
        self.Close()

class hostWindow(wx.Frame):
    def __init__(self, mw):
        self.mw = mw;
        super(hostWindow, self).__init__(parent=None, title='Host', size=(250,110), style = wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION)

        panel = wx.Panel(self)

        wx.StaticText(panel, pos=(25,11), label='Port:')
        self.portText = wx.TextCtrl(panel, pos=(55,10), size=(150,20))
        hostButton = wx.Button(panel, pos=(30,40), size=(170,25), label = 'Host')

        hostButton.Bind(wx.EVT_BUTTON, self.hostPressed)
        self.Show(True)

    def hostPressed(self, e):
        self.mw.chatText.write('Starting Server...\n')
        self.server = Server(int(self.portText.GetValue()), self.mw)
        self.mw.connectClient('localhost', int(self.portText.GetValue()))
        self.Close()

class nicknameWindow(wx.Frame):
    def __init__(self, mw):
        self.mw = mw;
        super(nicknameWindow, self).__init__(parent=None, title='Nickname', size=(250,110), style = wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION)

        panel = wx.Panel(self)

        wx.StaticText(panel, pos=(10,11), label='Nickname:')
        self.nickText = wx.TextCtrl(panel, pos=(75,10), size=(150,20))
        nickButton = wx.Button(panel, pos=(30,40), size=(170,25), label = 'Set Nickname')

        nickButton.Bind(wx.EVT_BUTTON, self.nickPressed)
        self.Show(True)

    def nickPressed(self, e):
        self.mw.client.sendMsg('_nick ' + self.nickText.GetValue())
        self.Close()

def main():
    app = wx.App()
    mainWindow()
    app.MainLoop()

main()
