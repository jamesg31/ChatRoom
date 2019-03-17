import wx
from chatroom import Client

class mainWindow(wx.Frame):
    def __init__(self):
        super(mainWindow, self).__init__(parent=None, title='Chat Room', size=(250,350), style = wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION)

        panel = wx.Panel(self)
        menuBar = wx.MenuBar()
        fileButton = wx.Menu()

        connectItem = fileButton.Append(wx.ID_ANY, 'Connect')
        hostItem = fileButton.Append(wx.ID_ANY, 'Host')
        exitItem = fileButton.Append(wx.ID_EXIT, 'Exit')
        menuBar.Append(fileButton, 'File')

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.ConnectMenu, connectItem)
        #self.Bind(wx.EVT_MENU, self.Host, hostItem)
        self.Bind(wx.EVT_MENU, self.Quit, exitItem)

        self.chatText = wx.TextCtrl(panel, pos=(10,10), size=(215,235), style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.inputText = wx.TextCtrl(panel, pos=(10,255), size=(150,25))
        inputButton = wx.Button(panel, pos=(170,255), size=(55,25), label = 'Send')
        self.chatText.Bind(wx.EVT_SET_FOCUS, self.Focus)
        inputButton.Bind(wx.EVT_BUTTON, self.SendPressed)
        self.Show(True)

    def Quit(self, e):
        self.Close()

    def Focus(self, e):
        return True

    def SendPressed(self, e):
        msg = self.inputText.GetValue()
        self.client.sendMsg(msg)
        self.inputText.SetValue('')

    def ConnectMenu(self, e):
        connectWindow(self)

    def ConnectClient(self, address, port):
        self.chatText.write('Connecting to server...\n')
        self.client = Client(address, int(port), self)

    def MessageRecieved(self, message):
        self.chatText.write(message + '\n')

#    def Host(self, e):

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

        connectButton.Bind(wx.EVT_BUTTON, self.ConnectPressed)
        self.Show(True)

    def ConnectPressed(self, e):
        self.mw.ConnectClient(self.hostText.GetValue(), self.portText.GetValue())
        self.Close()

def main():
    app = wx.App()
    mainWindow()
    app.MainLoop()

main()
