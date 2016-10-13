import socket
import threading
import wx


inString = ''
outString = ''
nick = ''
ip = ''
OutSign = 0


class TextFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'LoginFrame', size=(300, 110))
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
        global nick, ip
        nick = self.userText.GetValue()
        ip = self.ipText.GetValue()
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()


class ChatFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Chat Room', size=(500, 400))
        panel = wx.Panel(self, -1)

        self.OutLbl = wx.StaticText(panel, -1, 'Output Area:')
        self.OutTxt = wx.TextCtrl(
            panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(400, 300))
        self.InLbl = wx.StaticText(panel, -1, 'Input Area:')
        self.InTxt = wx.TextCtrl(panel, -1, size=(400, -1))
        self.InTxt.SetInsertionPoint(0)
        self.SendBtn = wx.Button(panel, -1, 'Send')
        self.Bind(wx.EVT_BUTTON, self.OnSendText, self.SendBtn)

        self.QuitBtn = wx.Button(panel, -1, 'Quit')
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.QuitBtn)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        sizer.AddMany([self.OutLbl,  self.OutTxt,
                       self.InLbl, self.InTxt,  self.QuitBtn, self.SendBtn])
        panel.SetSizer(sizer)

        self.Center()

    def OnSendText(self, event):
        global outString, OutSign
        outString = self.InTxt.GetValue()
        self.InTxt.Clear()
        OutSign = 1

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        global sock
        sock.close()
        self.Destroy()


class LoginApp(wx.App):

    def OnInit(self):
        frame = TextFrame()
        frame.Show(True)
        return True


class ChatApp(wx.App):

    def OnInit(self):
        self.frame = ChatFrame()
        self.frame.Show(True)
        return True


def DealOut(s):
    global nick, outString, OutSign
    while True:
        if OutSign:
            outString = nick + ': ' + outString
            s.send(outString)
            OutSign = 0


def DealIn(s, app):
    global inString
    while True:
        try:
            inString = s.recv(1024)
            if not inString:
                break
            if outString == inString:
                app.frame.OutTxt.AppendText('$' + inString + '\n')
            else:
                app.frame.OutTxt.AppendText(inString + '\n')
        except:
            break

app = LoginApp()
app.MainLoop()
del app

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, 8888))
sock.send(nick)

app = ChatApp()
thin = threading.Thread(target=DealIn, args=(sock, app,))
thin.start()
thout = threading.Thread(target=DealOut, args=(sock,))
thout.start()
app.MainLoop()
