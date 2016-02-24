# coding=utf-8
import time


class GameLogic(object):
    """
    docstring for GameLogic
    """

    def __init__(self, pipe):
        """
        docstring for __init__
        """
        super(GameLogic, self).__init__()

        self.pipe = pipe
        self.flag = {}
        self.flag["hitMyBat"] = False
        self.flag["hitYourBat"] = False
        self.flag["hitMyTable"] = False
        self.flag["hitYourTable"] = False
        self.flag["history"] = []

    def doLogic(self, setting, data):
        """
        docstring for doLogic
        """
        # 我板
        data["myBat"]["lastPos"] = data["myBat"]["pos"]
        data["myBat"]["pos"] = data["myMousePos"]
        if data["myBat"]["pos"][0] < setting["ScreenSize"][0] / 2 + setting["BatSize"][0] / 2:
            data["myBat"]["pos"][0] = setting["ScreenSize"][0] / 2 + setting["BatSize"][0] / 2
        # 你板
        data["yourBat"]["lastPos"] = data["yourBat"]["pos"]
        data["yourBat"]["pos"] = data["yourMousePos"]
        if data["yourBat"]["pos"][0] > setting["ScreenSize"][0] / 2 + setting["BatSize"][0] / 2:
            data["yourBat"]["pos"][0] = setting["ScreenSize"][0] / 2 - setting["BatSize"][0] / 2
        # 球的物理
        data["ball"]["speed"][1] += setting["Gravity"]
        data["ball"]["pos"][0] += data["ball"]["speed"][0]
        data["ball"]["pos"][1] += data["ball"]["speed"][1]
        # 碰撞地板
        if data["ball"]["pos"][1] + setting["BallSize"] > setting["ScreenSize"][1]:
            data["ball"]["pos"][1] = setting["ScreenSize"][1] - setting["BallSize"]
            data["ball"]["speed"][1] = -abs(data["ball"]["speed"][1]) * 0.9
            if data["ball"]["pos"][0] > setting["ScreenSize"][0] / 2:
                self.judge("hitRightBad")
            else:
                self.judge("hitLeftBad")
            dic = {}
            dic["cmd"] = "playSound"
            dic["data"] = ["pong", data["ball"]["pos"][0]]
            self.pipe(dic)
        """
        # 碰撞天花板
        if data["ball"]["pos"][1] - setting["BallSize"] < 0:
            data["ball"]["pos"][1] = setting["BallSize"]
            data["ball"]["speed"][1] = abs(data["ball"]["speed"][1]) * 0.9
            dic = {}
            dic["cmd"] = "playSound"
            dic["data"] = ["pong", data["ball"]["pos"][0]]
            self.pipe(dic)
        """
        # 碰撞桌面
        if (data["ball"]["pos"][1] + setting["BallSize"] > setting["ScreenSize"][1] - setting["TableSize"][1]
            and data["ball"]["pos"][0] + setting["BallSize"] > setting["ScreenSize"][0] / 2 - setting["TableSize"][0] / 2
            and data["ball"]["pos"][0] - setting["BallSize"] < setting["ScreenSize"][0] / 2 + setting["TableSize"][0] / 2):
            data["ball"]["pos"][1] = setting["ScreenSize"][1] - setting["TableSize"][1] - setting["BallSize"]
            data["ball"]["speed"][1] = -abs(data["ball"]["speed"][1]) * 0.9
            if data["ball"]["pos"][0] > setting["ScreenSize"][0] / 2:
                self.judge("hitRightTable")
            else:
                self.judge("hitLeftTable")
            dic = {}
            dic["cmd"] = "playSound"
            dic["data"] = ["pong", data["ball"]["pos"][0]]
            self.pipe(dic)
        # 碰撞左桌沿
        if (data["ball"]["pos"][0] + setting["BallSize"] > setting["ScreenSize"][0] / 2 - setting["TableSize"][0] / 2
            and data["ball"]["pos"][1] + setting["BallSize"] > setting["ScreenSize"][1] - setting["TableSize"][1]
            and data["ball"]["pos"][0] < setting["ScreenSize"][0] / 2):
            data["ball"]["pos"][0] = setting["ScreenSize"][0] / 2 - setting["TableSize"][0] / 2 - setting["BallSize"]
            data["ball"]["speed"][0] = -abs(data["ball"]["speed"][0]) * 0.9
            self.judge("hitLeftBad")
            dic = {}
            dic["cmd"] = "playSound"
            dic["data"] = ["pong", data["ball"]["pos"][0]]
            self.pipe(dic)
        # 碰撞右桌沿
        if (data["ball"]["pos"][0] - setting["BallSize"] < setting["ScreenSize"][0] / 2 + setting["TableSize"][0] / 2
            and data["ball"]["pos"][1] + setting["BallSize"] > setting["ScreenSize"][1] - setting["TableSize"][1]
            and data["ball"]["pos"][0] > setting["ScreenSize"][0] / 2):
            data["ball"]["pos"][0] = setting["ScreenSize"][0] / 2 + setting["TableSize"][0] / 2 + setting["BallSize"]
            data["ball"]["speed"][0] = abs(data["ball"]["speed"][0]) * 0.9
            self.judge("hitRightBad")
            dic = {}
            dic["cmd"] = "playSound"
            dic["data"] = ["pong", data["ball"]["pos"][0]]
            self.pipe(dic)
        # 碰撞右墙
        if data["ball"]["pos"][0] + setting["BallSize"] > setting["ScreenSize"][0]:
            data["ball"]["pos"][0] = setting["ScreenSize"][0] - setting["BallSize"]
            data["ball"]["speed"][0] = -abs(data["ball"]["speed"][0]) * 0.9
            self.judge("hitRightBad")
            dic = {}
            dic["cmd"] = "playSound"
            dic["data"] = ["pong", data["ball"]["pos"][0]]
            self.pipe(dic)
            if isinstance(data["yourScore"], str)  or isinstance(data["yourScore"], str):
                data["yourScore"], data["myScore"] = 0, 0
            if data["yourScore"] - data["myScore"] >= 5:
                dic = {}
                dic["cmd"] = "playSound"
                dic["data"] = ["a", data["ball"]["pos"][0]]
                self.pipe(dic)
            data["yourScore"] += 1
        # 碰撞左墙
        if data["ball"]["pos"][0] - setting["BallSize"] < 0:
            data["ball"]["pos"][0] = setting["BallSize"]
            data["ball"]["speed"][0] = abs(data["ball"]["speed"][0]) * 0.9
            self.judge("hitLeftBad")
            dic = {}
            dic["cmd"] = "playSound"
            dic["data"] = ["pong", data["ball"]["pos"][0]]
            self.pipe(dic)
            if isinstance(data["yourScore"], str)  or isinstance(data["yourScore"], str):
                data["yourScore"], data["myScore"] = 0, 0
            if data["myScore"] - data["yourScore"] >= 5:
                dic = {}
                dic["cmd"] = "playSound"
                dic["data"] = ["a", data["ball"]["pos"][0]]
                self.pipe(dic)
            data["myScore"] += 1
        # 球碰撞我板
        if (data["ball"]["pos"][0] > data["myBat"]["pos"][0] - setting["BallSize"] - setting["BatSize"][0] / 2
            and data["ball"]["pos"][0] < data["myBat"]["pos"][0] + setting["BallSize"] + setting["BatSize"][0] / 2
            and data["ball"]["pos"][1] > data["myBat"]["pos"][1] - setting["BallSize"] - setting["BatSize"][1] / 2
            and data["ball"]["pos"][1] < data["myBat"]["pos"][1] + setting["BallSize"] + setting["BatSize"][1] / 2):
            self.judge("hitRightBat")
            dic = {}
            dic["cmd"] = "playSound"
            dic["data"] = ["ping", data["ball"]["pos"][0]]
            self.pipe(dic)
            data["ball"]["pos"][0] = data["myBat"]["pos"][0] - setting["BallSize"] - setting["BatSize"][0] / 2
            data["ball"]["speed"][0] = (data["myBat"]["pos"][0] - data["myBat"]["lastPos"][0] - data["ball"]["speed"][0]) * setting["BatDecayRate"][0]
            data["ball"]["speed"][1] = (data["myBat"]["pos"][1] - data["myBat"]["lastPos"][1] + data["ball"]["speed"][1]) * setting["BatDecayRate"][1]
        # 球碰撞你板
        if (data["ball"]["pos"][0] > data["yourBat"]["pos"][0] - setting["BallSize"] - setting["BatSize"][0] / 2
            and data["ball"]["pos"][0] < data["yourBat"]["pos"][0] + setting["BallSize"] + setting["BatSize"][0] / 2
            and data["ball"]["pos"][1] > data["yourBat"]["pos"][1] - setting["BallSize"] - setting["BatSize"][1] / 2
            and data["ball"]["pos"][1] < data["yourBat"]["pos"][1] + setting["BallSize"] + setting["BatSize"][1] / 2):
            self.judge("hitLeftBat")
            dic = {}
            dic["cmd"] = "playSound"
            dic["data"] = ["ping", data["ball"]["pos"][0]]
            self.pipe(dic)
            data["ball"]["pos"][0] = data["yourBat"]["pos"][0] + setting["BallSize"] + setting["BatSize"][0] / 2
            data["ball"]["speed"][0] = (data["yourBat"]["pos"][0] - data["yourBat"]["lastPos"][0] - data["ball"]["speed"][0]) * setting["BatDecayRate"][0]
            data["ball"]["speed"][1] = (data["yourBat"]["pos"][1] - data["yourBat"]["lastPos"][1] + data["ball"]["speed"][1]) * setting["BatDecayRate"][1]
        # 球碰撞网
        if (data["ball"]["pos"][0] > setting["ScreenSize"][0] / 2 - setting["NetSize"][0] / 2 - setting["BallSize"]
            and data["ball"]["pos"][0] < setting["ScreenSize"][0] / 2 + setting["NetSize"][0] / 2 + setting["BallSize"]
            and data["ball"]["pos"][1] > setting["ScreenSize"][1] - setting["TableSize"][1] - setting["NetSize"][1] - setting["BallSize"]):
            if data["ball"]["speed"][0] > 0:
                data["ball"]["pos"][0] = setting["ScreenSize"][0] / 2 - setting["NetSize"][0] / 2 - setting["BallSize"]
                data["ball"]["speed"][0] = - data["ball"]["speed"][0]
            elif data["ball"]["speed"][0] < 0:
                data["ball"]["pos"][0] = setting["ScreenSize"][0] / 2 + setting["NetSize"][0] / 2 + setting["BallSize"]
                data["ball"]["speed"][0] = - data["ball"]["speed"][0]
            elif data["ball"]["speed"][0] == 0:
                data["ball"]["pos"][1] = setting["ScreenSize"][1] - setting["TableSize"][1] - setting["NetSize"][1] - setting["BallSize"]
                data["ball"]["speed"][1] = - data["ball"]["speed"][1]
            self.judge("hitNet")
        if isinstance(data["yourScore"], int) and isinstance(data["yourScore"], int) and (data["yourScore"] >= setting["WinScore"] or data["myScore"] >= setting["WinScore"]):
            if data["myScore"] >= setting["WinScore"]:
                data["yourScore"], data["myScore"] = "Lose", "Win"
                dic = {}
                dic["cmd"] = "playSound"
                dic["data"] = ["ha", setting["ScreenSize"][0]]
                self.pipe(dic)
                time.sleep(1)
                dic = {}
                dic["cmd"] = "playSound"
                dic["data"] = ["wu", 0]
                self.pipe(dic)
            else:
                data["yourScore"], data["myScore"] = "Win", "Lose"
                dic = {}
                dic["cmd"] = "playSound"
                dic["data"] = ["wu", setting["ScreenSize"][0]]
                self.pipe(dic)
                time.sleep(1)
                dic = {}
                dic["cmd"] = "playSound"
                dic["data"] = ["ha", 0]
                self.pipe(dic)
            data = self.doAStart(setting, data)
        return data

    def judge(self, event):
        """
        docstring for judge
        """
        # TODO
        print(event)
        if event == "hitRightBat":
            if self.flag["hitMyTable"] is True:  #
                self.flag["hitMyTable"] = False
            else:
                self.youGet()
        elif event == "hitLeftBat":
            if self.flag["hitYourTable"] is True:  #
                self.flag["hitYourTable"] = False
            else:
                self.iGet()
        elif event == "hitLeftTable":
            if self.flag["hitYourTable"] is True:  # hit your ground twice.
                self.iGet()
        elif event == "hitRightGround":
            if self.flag["hitMyTable"] is True:  # hit my ground twice.
                self.youGet()
            else:
                self.flag["hitMyTable"] = True
                self.flag["hitYourBat"] = False
        elif event == "hitRightBad":
            if self.flag["hitMyTable"] is True:
                self.youGet()
            else:
                self.iGet()
        elif event == "hitLeftBad":
            if self.flag["hitYourTable"] is True:
                self.iGet()
            else:
                self.youGet()
        elif event == "hitNet":
            if self.flag["hitMyBat"] is True:
                self.youGet()
            elif self.flag["hitYourBat"] is True:
                self.iGet()
            else:
                print("[WARN]Cannot judge.")
        self.flag["history"].append(event)

    def iGet(self):
        """
        docstring for Iget
        """
        print("IWin")
        self.flag["hitMyTable"] = False
        self.flag["hitYourTable"] = False
        self.flag["hitMyBat"] = False
        self.flag["hitYourBat"] = False

    def youGet(self):
        """
        docstring for youGet
        """
        print("youWin")
        self.flag["hitMyTable"] = False
        self.flag["hitYourTable"] = False
        self.flag["hitMyBat"] = False
        self.flag["hitYourBat"] = False

    def doAStart(self, setting, data):
        """
        docstring for doAStart
        """
        data["ball"]["pos"] = [setting["ScreenSize"][0] / 4 * 3, 100]
        data["ball"]["speed"] = [0, 0]
        data["ball"]["lastPos"] = [0, 0]
        return data
if __name__ == '__main__':
    I = GameLogic()
