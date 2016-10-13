import socket
import threading
import wx


inString = ''
outString = ''
nick = ''
ip = ''


class TextFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'LoginFrame', size=(300, 100))
        panel = wx.Panel(self, -1)
        self.userLabel = wx.StaticText(panel, -1, 'Nick Name:')
        self.userText = wx.TextCtrl(
            panel, -1, 'zhouwang', size=(175, -1))
        self.userText.SetInsertionPoint(0)

        self.ipLabel = wx.StaticText(panel, -1, 'IP address:')
        self.ipText = wx.TextCtrl(panel, -1, '115.159.31.135', size=(175, -1))

        self.entryBtn = wx.Button(panel, -1, "OK")
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.entryBtn)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        sizer.AddMany([self.userLabel, self.userText,
                       self.ipLabel, self.ipText, self.entryBtn])
        panel.SetSizer(sizer)

        self.Center()

    def OnCloseMe(self, event):
        global nick
        global ip
        nick = self.userText.GetValue()
        ip = self.ipText.GetValue()
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()


class LoginFrame(wx.App):

    def OnInit(self):
        frame = TextFrame()
        frame.Show(True)
        return True


def DealOut(s):
    global nick, outString
    while True:
        outString = raw_input()
        outString = nick + ': ' + outString
        s.send(outString)


def DealIn(s):
    global inString
    while True:
        try:
            inString = s.recv(1024)
            if not inString:
                break
            if outString != inString:
                print inString
        except:
            break

app = LoginFrame()
app.MainLoop()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, 8888))
sock.send(nick)

thin = threading.Thread(target=DealIn, args=(sock,))
thin.start()
thout = threading.Thread(target=DealOut, args=(sock,))
thout.start()
