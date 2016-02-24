# coding=utf-8
import lib_Display, lib_Net, lib_AI, lib_Sound, lib_GameLogic


class Game(object):
    """
    docstring for Game
    """

    def __init__(self, setting):
        """
        docstring for __init__
        """
        super(Game, self).__init__()

        self.setting = setting
        self.setting["BatDecayRate"] = [0.8, 1]
        self.setting["Gravity"] = 0.1
        self.setting["AIMaxSpeed"] = 10
        self.setting["AIHitDistance"] = 10
        self.setting["WinScore"] = 20
        self.setting["BallSize"] = 10
        self.setting["BatSize"] = [2, 80]
        self.setting["NetSize"] = [2, self.setting["ScreenSize"][1] / 8]
        self.setting["TableSize"] = [self.setting["ScreenSize"][0] / 2, self.setting["ScreenSize"][1] / 16]
        self.setting["NetDecayRate"] = [0.8, 1]

        self.data = {}
        self.data["ball"] = {}
        self.data["ball"]["pos"] = [self.setting["ScreenSize"][0] / 2, 100]
        self.data["ball"]["lastPos"] = [0, 0]
        self.data["ball"]["speed"] = [0, 0]
        self.data["myBat"] = {}
        self.data["myBat"]["pos"] = [self.setting["ScreenSize"][0] / 2, self.setting["ScreenSize"][1] / 2]
        self.data["myBat"]["lastPos"] = [self.setting["ScreenSize"][0] / 2, self.setting["ScreenSize"][1] / 2]
        self.data["yourBat"] = {}
        self.data["yourBat"]["pos"] = [self.setting["ScreenSize"][0] / 2, self.setting["ScreenSize"][1] / 2]
        self.data["yourBat"]["lastPos"] = [self.setting["ScreenSize"][0] / 2, self.setting["ScreenSize"][1] / 2]
        self.data["myScore"], self.data["yourScore"] = 0, 0
        if self.setting["DebugMode"] is True:
            self.data["debug"] = {}
            self.data["debug"]["pathPointList"] = []
            self.data["debug"]["hitPoint"] = [0, 0]
            self.data["debug"]["startPoint"] = [0, 0]
            self.data["debug"]["targetPoint"] = [0, 0]

        self.ai = lib_AI.AI()
        self.net = lib_Net.Net()
        self.sound = lib_Sound.Sound()
        self.display = lib_Display.Display(self.pipe)
        self.gameLogic = lib_GameLogic.GameLogic(self.pipe)

        self.setting["MyName"] = input('请输入玩家名字：')
        mode = input('请输入模式(\n输入“s”进入单人模式\n输入“h”进入多人模式，并建立主机\n输入“c”进入多人模式，并做客户端)\n：')
        if mode == "s":
            self.setting["Mode"] = "SinglePlayer"
            self.setting["YourName"] = "Computer"
        elif mode == "h":
            self.setting["Mode"] = "Server"
            print("本机IP：%s" % self.net.getMyIP())
            port = input("请输入端口号(默认50000)：")
            if port == "":
                port = "50000"
            self.net.startServer(int(port))
            self.net.sendMsg(self.setting["MyName"])
            self.setting["YourName"] = self.net.recvMsg()
        elif mode == "c":
            self.setting["Mode"] = "Client"
            print("本机IP：%s" % self.net.getMyIP())
            host = input("请输入IP(默认本机IP)：")
            if host == "":
                host = self.net.getMyIP()
            port = input("请输入端口号(默认50000)：")
            if port == "":
                port = "50000"
            self.net.connect(host, int(port))
            self.setting["YourName"] = self.net.recvMsg()
            self.net.sendMsg(self.setting["MyName"])
        else:
            print("[WARN]")

        self.display.init(self.setting)

        self.display.run()
    def pipe(self, data):
        """
        (data:dict)
        return *
        """
        if data["cmd"] == "getData":
            return self.data
        elif data["cmd"] == "update":
            self.update()
        elif data["cmd"] == "sendMsg":
            self.net.sendMsg(data["data"])
        elif data["cmd"] == "doAStart":
            self.gameLogic.doAStart(self.setting, self.data)
        elif data["cmd"] == "playSound":
            if data["data"][0] == "a":
                data["data"][0] = self.sound.sound_a
            elif data["data"][0] == "ha":
                data["data"][0] = self.sound.sound_ha
            elif data["data"][0] == "ping":
                data["data"][0] = self.sound.sound_ping
            elif data["data"][0] == "pong":
                data["data"][0] = self.sound.sound_pong
            elif data["data"][0] == "wu":
                data["data"][0] = self.sound.sound_wu
            self.sound.playSound(self.setting, data["data"][0], data["data"][1])
        else:
            print("[WARN]")

    def update(self):
        """
        docstring for update
        """
        self.data["myMousePos"] = self.display.mousePos
        if self.setting["Mode"] == "SinglePlayer":
            self.data["yourMousePos"] = self.ai.doAI(self.setting, self.data)
            self.data = self.gameLogic.doLogic(self.setting, self.data)
        elif self.setting["Mode"] == "Server":
            self.data["yourMousePos"] = self.net.getClientData(self.setting, self.data)
            self.data = self.gameLogic.doLogic(self.setting, self.data)
            self.net.sendServerData(self.data)
        elif self.setting["Mode"] == "Client":
            self.data = self.net.getServerData(self.setting, self.data)
            self.data["myBat"]["lastPos"] = self.data["myBat"]["pos"]
            self.data["myBat"]["pos"] = self.data["myMousePos"]
            if self.data["myBat"]["pos"][0] < self.setting["ScreenSize"][0] / 2 + self.setting["BatSize"][0] / 2:
                self.data["myBat"]["pos"][0] = self.setting["ScreenSize"][0] / 2 + self.setting["BatSize"][0] / 2
            self.net.sendClientData(self.data)
if __name__ == '__main__':
    DebugSetting = {}
    DebugSetting["ScreenSize"] = [1366, 768]
    DebugSetting["Title"] = "Hello"
    DebugSetting["DebugMode"] = False
    I = Game(DebugSetting)
