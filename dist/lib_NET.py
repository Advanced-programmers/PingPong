#coding=utf-8
import time, socket
class NET():
    """
    docstring for NET
    """
    myMode = ""
    myData = ("", 50000)
    yourData = ("", 50000)

    def __init__(self):

        self.isRunning = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        if self.myMode == "server":
            try:
                self.s.bind(self.myData)
                self.s.listen(1)
            except OSError as e:
                print("[WARN]" + str(e))
                print("[    ]lib_NET.NET.run()")
                print("[    ]self.s.bind(self.myData)")
                print("[    ]self.myData = " + str(self.myData))
            finally:
                pass
            print("[INFO]已启动服务器于：" + self.myData[0] + ":" + str(self.myData[1]))
            print("[INFO]等待请求中……")
            self.c, a = self.s.accept()
            print("[INFO]已捕获连接请求！正在连接……")
            self.yourData = a
            print('[FINE]连接成功：' + self.yourData[0] + ":" + str(self.yourData[1]))
            self.doServer()
            #self.c.close()
        elif self.myMode == "client":
            print("[INFO]正在连接：" + self.yourData[0] + ":" + str(self.yourData[1]))
            try:
                self.s.connect(self.yourData)
                print("[FINE]连接成功！")
            except OSError as e:
                print("[WARN]" + str(e))
                print("[    ]lib_NET.NET.run()")
                print("[    ]self.s.connect(self.yourData)")
                print("[    ]self.yourData = " + str(self.yourData))
            finally:
                pass
            self.doClient()
        else:
            pass
    def doServer(self):
        pass
    def doClient(self):
        pass
    def getMyIP(self):
        return socket.gethostbyname(socket.gethostname())
    def startServer(self, myPort):
        self.myMode = "server"
        self.myData = (self.getMyIP(), myPort)
        self.run()
    def connect(self, yourIP, yourPort):
        self.myMode = "client"
        self.yourData = (yourIP, yourPort)
        self.run()
    def recv(self):
        if self.myMode == "server":
            try:
                return self.c.recv(4096)
            except OSError as e:
                print("[WARN]" + str(e))
                print("[    ]lib_NET.NET.recv()")
                print("[    ]return self.c.recv(4096)")
        elif self.myMode == "client":
            try:
                return self.s.recv(4096)
            except OSError as e:
                print("[WARN]" + str(e))
                print("[    ]lib_NET.NET.recv()")
                print("[    ]return self.s.recv(4096)")
        else:
            pass
    def send(self, data):
        if self.myMode == "server":
            try:
                self.c.send(data)
            except OSError as e:
                print("[WARN]" + str(e))
                print("[    ]lib_NET.NET.send()")
                print("[    ]self.c.send(data)")
                print("[    ]data = " + str(data))
        elif self.myMode == "client":
            try:
                self.s.send(data)
            except OSError as e:
                print("[WARN]" + str(e))
                print("[    ]lib_NET.NET.send()")
                print("[    ]self.s.send(data)")
                print("[    ]data = " + str(data))
        else:
            pass
    def recvMsg(self):
        return self.recv().decode("utf-8")
    def sendMsg(self, data):
        self.send(data.encode("utf-8"))
if __name__ == '__main__':
    S = NET()
    C = NET()
    S.startServer(50000)
    #time.sleep(1)
    C.connect(C.getMyIP(), 50000)
