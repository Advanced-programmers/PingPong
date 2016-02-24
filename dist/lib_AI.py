# coding=utf-8
from math import *


class AI(object):
    """
    docstring for AI
    """

    def __init__(self):
        """
        docstring for __init__
        """
        super(AI, self).__init__()

        self.flag = {}
        self.flag["hasShowDebugInfo"] = False

    def doAI(self, setting, data):
        """
        (设定:dic, 即时数据:dic)
        return [yourBat.pos.x:int, yourBat.pos.y:int]
        """
        self.setting = setting
        self.data = data
        # 局势判断
        if data["ball"]["pos"][0] <= setting["ScreenSize"][0] / 2 and data["ball"]["speed"][0] >= 0:
            # 返回
            return self.AIMoveTo(data["yourBat"]["pos"][0], data["yourBat"]["pos"][1], 64)
        elif data["ball"]["pos"][0] >= setting["ScreenSize"][0] / 2 and data["ball"]["speed"][0] >= 0:
            # 恢复
            return self.AIMoveTo(setting["ScreenSize"][0] / 3, (setting["ScreenSize"][1] / 2 + data["ball"]["pos"][1]) / 2, 32)
        elif data["ball"]["pos"][0] >= setting["ScreenSize"][0] / 2 and data["ball"]["speed"][0] <= 0:
            # 准备
            return self.AIMoveTo(setting["ScreenSize"][0] / 3, data["ball"]["pos"][1], 32)
        elif data["ball"]["pos"][0] <= setting["ScreenSize"][0] / 8 and data["ball"]["speed"][0] <= 0:
            # 击打
            if self.AIGetInfo()[2] <= setting["AIHitDistance"]:
                return self.AIMoveTo(data["ball"]["pos"][0] + setting["AIHitDistance"], data["ball"]["pos"][1], 1)
            else:
                return self.AIMoveTo(data["ball"]["pos"][0] - setting["AIHitDistance"], data["ball"]["pos"][1] + data["ball"]["speed"][1], 8)
        elif data["ball"]["pos"][0] <= setting["ScreenSize"][0] / 2 and data["ball"]["speed"][0] <= 0:
            # 击打
            if self.AIGetInfo()[2] <= setting["AIHitDistance"]:
                return self.AIMoveTo(data["ball"]["pos"][0] + setting["AIHitDistance"], data["ball"]["pos"][1], 1)
            else:
                return self.AIMoveTo(data["ball"]["pos"][0] - setting["BallSize"] - setting["AIHitDistance"] + data["ball"]["speed"][0] * 10, data["ball"]["pos"][1] + data["ball"]["speed"][1] * 10, 8)
    def AIGetInfo(self):
        """
        获取AI.Bat与Ball之间的相对距离。
        ()
        return [相对水平距离:int, 相对垂直距离:int, 相对距离:int]
        """
        deltaX, deltaY = self.data["ball"]["pos"][0] - self.data["yourBat"]["pos"][0],  self.data["ball"]["pos"][1] - self.data["yourBat"]["pos"][1]
        delta = hypot(deltaX, deltaY)
        return [deltaX, deltaY, delta]
    def AIMoveTo(self, x, y, rate):
        """
        docstring for AIMoveTo
        """
        deltaX, deltaY = x - self.data["yourBat"]["pos"][0], y - self.data["yourBat"]["pos"][1]
        delta = hypot(deltaX, deltaY)
        return self.AIMove(x - self.data["yourBat"]["pos"][0], y - self.data["yourBat"]["lastPos"][1], delta / rate)
    def AIMove(self, x, y, speed):
        """
        docstring for AIMove
        """
        if speed > self.setting["AIMaxSpeed"]:
            speed = self.setting["AIMaxSpeed"]
        a = hypot(x, y) + 0.001
        tX, tY = speed * x / a, speed * y / a
        self.data["yourBat"]["pos"] = [tX + self.data["yourBat"]["lastPos"][0], tY + self.data["yourBat"]["lastPos"][1]]
        return self.data["yourBat"]["pos"]
if __name__ == '__main__':
    I = AI()
