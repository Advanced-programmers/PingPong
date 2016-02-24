# coding=utf-8
import time, pygame
import ori_Display


class Display(ori_Display.Display):
    """
    docstring for Display
    """

    def __init__(self, pipe):
        """
        docstring for __init__
        """
        super(Display, self).__init__()
        self.pipe = pipe

    def init(self, setting):
        """
        docstring for init
        """
        self.setting = setting
        self.createWindow(setting["ScreenSize"])
        self.setTitle(setting["Title"])

        self.ball = pygame.Surface((setting["BallSize"] * 2, setting["BallSize"] * 2))
        self.ball.fill(self.WHITE)
        pygame.draw.circle(self.ball, self.RED, [setting["BallSize"], setting["BallSize"]], setting["BallSize"])

        self.myBat = pygame.Surface(setting["BatSize"])
        self.myBat.fill(self.BLACK)

        self.yourBat = pygame.Surface(setting["BatSize"])
        self.yourBat.fill(self.BLACK)

        self.net = pygame.Surface(setting["NetSize"])
        self.net.fill(self.BLACK)

        self.table = pygame.Surface(setting["TableSize"])
        self.net.fill(self.BLACK)
        pygame.draw.rect(self.table, self.WHITE, pygame.locals.Rect((2, 2), (setting["TableSize"][0] - 4, setting["TableSize"][1] - 2)))

        if self.setting["DebugMode"] is True:
            self.pathPoint = pygame.Surface([1, 1])
            self.pathPoint.fill(self.BLACK)

            self.startPoint = pygame.Surface((setting["BallSize"][0] * 2, setting["BallSize"][1] * 2))
            self.startPoint.fill(self.Red)
            self.hitPoint = pygame.Surface((setting["BallSize"][0] * 2, setting["BallSize"][1] * 2))
            self.hitPoint.fill(self.GREEN)
            self.targetPoint = pygame.Surface((setting["BallSize"][0] * 2, setting["BallSize"][1] * 2))
            self.targetPoint.fill(self.BLUE)

    def setup(self):
        """
        docstring for setup
        """
        pygame.mouse.set_visible(False)

        if self.setting["Mode"] == "SinglePlayer":
            self.setTitle("SinglePlayer (Press right mouse button to reset ball.)")
        elif self.setting["Mode"] == "Server":
            self.setTitle("Server (Press right mouse button to reset ball.)")
        elif self.setting["Mode"] == "Client":
            self.setTitle("Client (Press right mouse button to reset ball.)")

        dic = {}
        dic["cmd"] = "getData"
        self.data = self.pipe(dic)

        self.screen.fill(self.WHITE)

        try:
            self.font = pygame.font.Font("res\\Ubuntu-R.ttf", 32)
        except OSError as e:
            print("[WARN][Game.Game.setup]" + str(e))
            print("[    ]self.font = pygame.font.Font('Ubuntu-R.ttf', 32)")
        finally:
            pass
        if self.setting["Mode"] == "Server":
            newData = "%s|%s|%s|%s|%s|%s" % (self.data["ball"]["pos"][0], self.data["ball"]["pos"][1], self.data["myBat"]["pos"][0], self.data["myBat"]["pos"][1], self.data["myScore"], self.data["yourScore"])
            print("Server send data:%s"%str(newData))
            dic = {}
            dic["cmd"] = "sendMsg"
            dic["data"] = newData
            self.data = self.pipe(dic)

    def main(self):
        """
        docstring for main
        """
        self.screen.fill(self.WHITE)

        dic = {}
        dic["cmd"] = "update"
        self.pipe(dic)

        dic = {}
        dic["cmd"] = "getData"
        self.data = self.pipe(dic)

        # 绘制
        score = self.font.render("%s : %s" % (self.data["yourScore"], self.data["myScore"]), True, self.BLACK, self.WHITE)
        if self.setting["DebugMode"] is True:
            for eachPathPoint in self.data["debug"]["pathPointList"]:
                self.screen.blit(self.pathPoint, eachPathPoint)
            self.screen.blit(self.startPoint, self.data["debug"]["startPoint"])
            self.screen.blit(self.hitPoint, self.data["debug"]["hitPoint"])
            self.screen.blit(self.targetPoint, self.data["debug"]["targetPoint"])
        self.screen.blit(self.table, (self.setting["ScreenSize"][0] / 2 - self.setting["TableSize"][0] / 2, self.setting["ScreenSize"][1] - self.setting["TableSize"][1]))
        self.screen.blit(self.net, (self.setting["ScreenSize"][0] / 2 - self.setting["NetSize"][0] / 2, self.setting["ScreenSize"][1] - self.setting["NetSize"][1] - self.setting["TableSize"][1]))
        self.screen.blit(self.ball, (self.data["ball"]["pos"][0] - self.setting["BallSize"], self.data["ball"]["pos"][1] - self.setting["BallSize"]))
        self.screen.blit(self.myBat, (self.data["myBat"]["pos"][0] - self.setting["BatSize"][0] / 2, self.data["myBat"]["pos"][1] - self.setting["BatSize"][1] / 2))
        self.screen.blit(self.yourBat, (self.data["yourBat"]["pos"][0] - self.setting["BatSize"][0] / 2, self.data["yourBat"]["pos"][1] - self.setting["BatSize"][1] / 2))
        self.screen.blit(score, (self.setting["ScreenSize"][0] / 2 - score.get_width() / 2, 0))

    def doMouseButtonUp(self, button):
        """
        docstring for doMouseButtonUp
        """
        if button == 3:
            dic = {}
            dic["cmd"] = "doAStart"
            self.pipe(dic)
if __name__ == '__main__':
    I = Display()
