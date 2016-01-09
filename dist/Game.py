#coding=utf-8
import pygame, random, time
from math import *
from pygame.locals import *
import lib_Display, lib_NET
class Game(lib_Display.Display):
    """docstring for Game"""
    def __init__(self):
        super(Game, self).__init__()
    def init(self):
        self.batDecayRate = [0.8, 1]
        self.Gravity = 0.05
        self.yourScore, self.myScore = 0, 0
        self.AIMaxSpeed = 10
        self.AITmpData = []
        self.winScore = 20
        self.net = lib_NET.NET()
        self.mode = input('请输入模式\n(输入“s”进入单人模式\n输入“h”进入多人模式，并建立主机\n输入“c”进入多人模式，并做客户端)\n：')
        if self.mode == "s":
            pass
        elif self.mode == "h":
            print("本机IP：%s" % self.net.getMyIP())
            port = input("请输入端口号(默认50000)：")
            if port == "":
                port = "50000"
            self.net.startServer(int(port))
        elif self.mode == "c":
            print("本机IP：%s" % self.net.getMyIP())
            host = input("请输入IP(默认本机IP)：")
            if host == "":
                host = self.net.getMyIP()
            port = input("请输入端口号(默认50000)：")
            if port == "":
                port = "50000"
            self.net.connect(host, int(port))
    def setup(self):
        pygame.mouse.set_visible(False)

        self.sound_ping = pygame.mixer.Sound("ping.wav")
        self.sound_pong = pygame.mixer.Sound("pong.wav")
        self.sound_a = pygame.mixer.Sound("a.wav")
        self.sound_wu = pygame.mixer.Sound("wu.wav")
        self.sound_ha = pygame.mixer.Sound("ha.wav")

        if self.mode == "s":
            self.setTitle("SinglePlayer")
        elif self.mode == "ms":
            self.setTitle("Server")
        elif self.mode == "mc":
            self.setTitle("Client")

        self.ballData = [[self.screenSize[0] / 2, 100], 10, [0, 0]]
        self.myBatData = [[0, 0], (2, 80), [0, 0]]
        self.yourBatData = [[100, 100], self.myBatData[1], [0, 0]]

        self.screen.fill([255,255,255])

        self.ball = pygame.Surface((self.ballData[1] * 2, self.ballData[1] * 2))
        self.ball.fill([255,255,255])
        pygame.draw.circle(self.ball, [255, 0, 0], [self.ballData[1], self.ballData[1]], self.ballData[1])
        self.screen.blit(self.ball, (0, 0))

        self.myBat = pygame.Surface(self.myBatData[1])
        self.myBat.fill([0,0,0])

        self.yourBat = pygame.Surface(self.yourBatData[1])
        self.yourBat.fill([0,0,0])

        try:
            self.font = pygame.font.Font("Ubuntu-R.ttf", 32)
        except OSError as e:
            print("[WARN]" + str(e))
            print("[    ]Game.Game.setup()")
            print("[    ]self.font = pygame.font.Font('Ubuntu-R.ttf', 32)")
        finally:
            pass

        if self.mode == "ms":
            newData = "%s|%s|%s|%s|%s|%s" % (self.ballData[0][0], self.ballData[0][1], self.myBatData[0][0], self.myBatData[0][1], self.myScore, self.yourScore)
            print("Server send data:%s"%str(newData))
            self.net.sendMsg(newData)
    def main(self):
        #
        self.screen.fill([255,255,255])
        #
        if self.mode == "s":
            # 我板
            self.myBatData[2] = self.myBatData[0]
            self.myBatData[0] = [self.mousePos[0], self.mousePos[1]]
            if self.myBatData[0][0] < self.screenSize[0] / 2 + self.myBatData[1][0] / 2:
                self.myBatData[0][0] = self.screenSize[0] / 2 + self.myBatData[1][0] / 2
            # 你板
            self.yourBatData[2] = self.yourBatData[0]
            self.doAI()
            if self.yourBatData[0][0] > self.screenSize[0] / 2 + self.yourBatData[1][0] / 2:
                self.yourBatData[0][0] = self.screenSize[0] / 2 - self.yourBatData[1][0] / 2
            # 球的物理
            self.ballData[2][1] += self.Gravity
            self.ballData[0][0] += self.ballData[2][0]
            self.ballData[0][1] += self.ballData[2][1]
            # 碰撞地板
            if self.ballData[0][1] + self.ballData[1] > self.screenSize[1]:
                self.ballData[0][1] = self.screenSize[1] - self.ballData[1]
                self.ballData[2][1] = -abs(self.ballData[2][1]) * 0.9
                self.playSound(self.sound_pong, self.ballData[0][0])
            # 碰撞天花板
            if self.ballData[0][1] - self.ballData[1] < 0:
                self.ballData[0][1] = self.ballData[1]
                self.ballData[2][1] = abs(self.ballData[2][1]) * 0.9
                self.playSound(self.sound_pong, self.ballData[0][0])
            # 碰撞右墙
            if self.ballData[0][0] + self.ballData[1] > self.screenSize[0]:
                self.ballData[0][0] = self.screenSize[0] - self.ballData[1]
                self.ballData[2][0] = -abs(self.ballData[2][0]) * 0.9
                self.playSound(self.sound_pong, self.ballData[0][0])
                if isinstance(self.yourScore, str)  or isinstance(self.yourScore, str):
                    self.yourScore, self.myScore = 0, 0
                if self.yourScore - self.myScore >= 5:
                    self.playSound(self.sound_a, self.screenSize[0])
                self.yourScore += 1
            # 碰撞左墙
            if self.ballData[0][0] - self.ballData[1] < 0:
                self.ballData[0][0] = self.ballData[1]
                self.ballData[2][0] = abs(self.ballData[2][0]) * 0.9
                self.playSound(self.sound_pong, self.ballData[0][0])
                if isinstance(self.yourScore, str)  or isinstance(self.yourScore, str):
                    self.yourScore, self.myScore = 0, 0
                if self.myScore - self.yourScore >= 5:
                    self.playSound(self.sound_a, 0)
                self.myScore += 1
            # 球碰撞我板
            if (self.ballData[0][0] > self.myBatData[0][0] - self.ballData[1] - self.myBatData[1][0] / 2
                and self.ballData[0][0] < self.myBatData[0][0] + self.ballData[1] + self.myBatData[1][0] / 2
                and self.ballData[0][1] > self.myBatData[0][1] - self.ballData[1] - self.myBatData[1][1] / 2
                and self.ballData[0][1] < self.myBatData[0][1] + self.ballData[1] + self.myBatData[1][1] / 2):
                self.playSound(self.sound_ping, self.ballData[0][0])
                self.ballData[0][0] = self.myBatData[0][0] - self.ballData[1] - self.myBatData[1][0] / 2
                self.ballData[2][0] = (self.myBatData[0][0] - self.myBatData[2][0] - self.ballData[2][0]) * self.batDecayRate[0]
                self.ballData[2][1] = (self.myBatData[0][1] - self.myBatData[2][1] + self.ballData[2][1]) * self.batDecayRate[1]
            # 球碰撞你板
            if (self.ballData[0][0] > self.yourBatData[0][0] - self.ballData[1] - self.yourBatData[1][0] / 2
                and self.ballData[0][0] < self.yourBatData[0][0] + self.ballData[1] + self.yourBatData[1][0] / 2
                and self.ballData[0][1] > self.yourBatData[0][1] - self.ballData[1] - self.yourBatData[1][1] / 2
                and self.ballData[0][1] < self.yourBatData[0][1] + self.ballData[1] + self.yourBatData[1][1] / 2):
                self.playSound(self.sound_ping, self.ballData[0][0])
                self.ballData[0][0] = self.yourBatData[0][0] + self.ballData[1] + self.yourBatData[1][0] / 2
                self.ballData[2][0] = (self.yourBatData[0][0] - self.yourBatData[2][0] - self.ballData[2][0]) * self.batDecayRate[0]
                self.ballData[2][1] = (self.yourBatData[0][1] - self.yourBatData[2][1] + self.ballData[2][1]) * self.batDecayRate[1]
            if isinstance(self.yourScore, int) and isinstance(self.yourScore, int) and (self.yourScore >= self.winScore or self.myScore >= self.winScore):
                if self.myScore >= self.winScore:
                    self.yourScore, self.myScore = "Lose", "Win"
                    self.playSound(self.sound_ha, self.screenSize[0])
                    time.sleep(1)
                    self.playSound(self.sound_wu, 0)
                else:
                    self.yourScore, self.myScore = "Win", "Lose"
                    self.playSound(self.sound_wu, self.screenSize[0])
                    time.sleep(1)
                    self.playSound(self.sound_ha, 0)
                self.ballData = [[self.screenSize[0] / 2, 100], 10, [0, 0]]
        elif self.mode == "ms":
            data = self.net.recvMsg()
            print("Server recv data:%s"%str(data))
            yourX, yourY = data.split("|")
            # 我板
            self.myBatData[2] = self.myBatData[0]
            self.myBatData[0] = [self.mousePos[0], self.mousePos[1]]
            if self.myBatData[0][0] < self.screenSize[0] / 2 + self.myBatData[1][0] / 2:
                self.myBatData[0][0] = self.screenSize[0] / 2 + self.myBatData[1][0] / 2
            # 你板
            self.yourBatData[2] = self.yourBatData[0]
            self.yourBatData[0] = [self.screenSize[0] - float(yourX), float(yourY)]
            if self.yourBatData[0][0] > self.screenSize[0] / 2 + self.yourBatData[1][0] / 2:
                self.yourBatData[0][0] = self.screenSize[0] / 2 - self.yourBatData[1][0] / 2
            # 球的物理
            self.ballData[2][1] += self.Gravity
            self.ballData[0][0] += self.ballData[2][0]
            self.ballData[0][1] += self.ballData[2][1]
            # 碰撞地板
            if self.ballData[0][1] + self.ballData[1] > self.screenSize[1]:
                self.ballData[0][1] = self.screenSize[1] - self.ballData[1]
                self.ballData[2][1] = -abs(self.ballData[2][1]) * 0.9
            # 碰撞天花板
            if self.ballData[0][1] - self.ballData[1] < 0:
                self.ballData[0][1] = self.ballData[1]
                self.ballData[2][1] = abs(self.ballData[2][1]) * 0.9
            # 碰撞右墙
            if self.ballData[0][0] + self.ballData[1] > self.screenSize[0]:
                self.ballData[0][0] = self.screenSize[0] - self.ballData[1]
                self.ballData[2][0] = -abs(self.ballData[2][0]) * 0.9
                if isinstance(self.yourScore, str)  or isinstance(self.yourScore, str):
                    self.yourScore, self.myScore = 0, 0
                self.yourScore += 1
            # 碰撞左墙
            if self.ballData[0][0] - self.ballData[1] < 0:
                self.ballData[0][0] = self.ballData[1]
                self.ballData[2][0] = abs(self.ballData[2][0]) * 0.9
                if isinstance(self.yourScore, str)  or isinstance(self.yourScore, str):
                    self.yourScore, self.myScore = 0, 0
                self.myScore += 1
            # 球碰撞我板
            if (self.ballData[0][0] > self.myBatData[0][0] - self.ballData[1] - self.myBatData[1][0] / 2
                and self.ballData[0][0] < self.myBatData[0][0] + self.ballData[1] + self.myBatData[1][0] / 2
                and self.ballData[0][1] > self.myBatData[0][1] - self.ballData[1] - self.myBatData[1][1] / 2
                and self.ballData[0][1] < self.myBatData[0][1] + self.ballData[1] + self.myBatData[1][1] / 2):

                self.ballData[0][0] = self.myBatData[0][0] - self.ballData[1] - self.myBatData[1][0] / 2
                self.ballData[2][0] = (self.myBatData[0][0] - self.myBatData[2][0] - self.ballData[2][0]) * self.batDecayRate[0]
                self.ballData[2][1] = (self.myBatData[0][1] - self.myBatData[2][1] + self.ballData[2][1]) * self.batDecayRate[1]
            # 球碰撞你板
            if (self.ballData[0][0] > self.yourBatData[0][0] - self.ballData[1] - self.yourBatData[1][0] / 2
                and self.ballData[0][0] < self.yourBatData[0][0] + self.ballData[1] + self.yourBatData[1][0] / 2
                and self.ballData[0][1] > self.yourBatData[0][1] - self.ballData[1] - self.yourBatData[1][1] / 2
                and self.ballData[0][1] < self.yourBatData[0][1] + self.ballData[1] + self.yourBatData[1][1] / 2):

                self.ballData[0][0] = self.yourBatData[0][0] + self.ballData[1] + self.yourBatData[1][0] / 2
                self.ballData[2][0] = (self.yourBatData[0][0] - self.yourBatData[2][0] - self.ballData[2][0]) * self.batDecayRate[0]
                self.ballData[2][1] = (self.yourBatData[0][1] - self.yourBatData[2][1] + self.ballData[2][1]) * self.batDecayRate[1]
            if isinstance(self.yourScore, int) and isinstance(self.yourScore, int) and (self.yourScore >= self.winScore or self.myScore >= self.winScore):
                if self.myScore >= self.winScore:
                    self.yourScore, self.myScore = "Lose", "Win"
                else:
                    self.yourScore, self.myScore = "Win", "Lose"
                self.ballData = [[self.screenSize[0] / 2, 100], 10, [0, 0]]
            # newData
            newData = "%s|%s|%s|%s|%s|%s" % (self.ballData[0][0], self.ballData[0][1], self.myBatData[0][0], self.myBatData[0][1], self.myScore, self.yourScore)
            print("Server send data:%s"%str(newData))
            self.net.sendMsg(newData)
        elif self.mode == "mc":
            data = self.net.recvMsg()
            print("Client recv data:%s"%str(data))
            ballX, ballY, yourX, yourY, yourScore, myScore = data.split("|")
            self.ballData[0][0] = self.screenSize[0] - float(ballX)
            self.ballData[0][1] = float(ballY)
            self.yourBatData[0][0] = self.screenSize[0] - float(yourX)
            self.yourBatData[0][1] = float(yourY)
            if myScore.isdigit() or yourScore.isdigit():
                self.myScore = int(myScore)
                self.yourScore = int(yourScore)
            else:
                self.myScore = myScore
                self.yourScore = yourScore
            # 我板
            self.myBatData[2] = self.myBatData[0]
            self.myBatData[0] = [self.mousePos[0], self.mousePos[1]]
            if self.myBatData[0][0] < self.screenSize[0] / 2 + self.myBatData[1][0] / 2:
                self.myBatData[0][0] = self.screenSize[0] / 2 + self.myBatData[1][0] / 2
            # newData
            newData = "%s|%s" % (self.myBatData[0][0], self.myBatData[0][1])
            print("Client send data:%s"%str(newData))
            self.net.sendMsg(newData)
        #

        score = self.font.render("%s : %s" % (self.yourScore, self.myScore), True, (0,0,0), (255, 255, 255))
        self.screen.blit(self.ball, (self.ballData[0][0] - self.ballData[1], self.ballData[0][1] - self.ballData[1]))
        self.screen.blit(self.myBat, (self.myBatData[0][0] - self.myBatData[1][0] / 2, self.myBatData[0][1] - self.myBatData[1][1] / 2))
        self.screen.blit(self.yourBat, (self.yourBatData[0][0] - self.yourBatData[1][0] / 2, self.yourBatData[0][1] - self.yourBatData[1][1] / 2))
        self.screen.blit(score, (self.screenSize[0] / 2 - score.get_width() / 2, 0))
    def doMouseButtonUp(self, button):
        if button == 3:
            self.ballData = [[self.screenSize[0] / 2, 100], 10, [0, 0]]
    def doAI(self):
        # 局势判断
        if self.ballData[0][0] <= self.screenSize[0] / 2 and self.ballData[2][0] >= 0:
            # 返回
            self.AIMoveTo(self.screenSize[0] / 16, self.screenSize[1] / 2, 1)
        elif self.ballData[0][0] >= self.screenSize[0] / 2 and self.ballData[2][0] >= 0:
            # 恢复
            self.AIMoveTo(self.screenSize[0] / 16, (self.screenSize[1] / 2 + self.ballData[0][1]) / 2, 1)
        elif self.ballData[0][0] >= self.screenSize[0] / 2 and self.ballData[2][0] <= 0:
            # 准备
            self.AIMoveTo(self.screenSize[0] / 16, self.ballData[0][1], 1)
        elif self.ballData[0][0] <= self.screenSize[0] / 2 and self.ballData[2][0] <= 0:
            # 击打
            self.AIMoveTo(self.screenSize[0] / 16, self.ballData[0][1], 1)
            if self.AIGetInfo()[2] <= 100:
                self.AIMoveTo(self.ballData[0][0] + 200, self.ballData[0][1], 1)
    def AIGetInfo(self):
        deltaX, deltaY = self.ballData[0][0] - self.yourBatData[0][0],  self.ballData[0][1] - self.yourBatData[0][1]
        delta = hypot(deltaX, deltaY)
        return [deltaX, deltaY, delta]
    def AIMoveTo(self, x, y, speed):
        deltaX, deltaY = x - self.yourBatData[0][0], y - self.yourBatData[0][1]
        delta = hypot(deltaX, deltaY)
        self.AIMove(x - self.yourBatData[2][0], y - self.yourBatData[2][1], delta / 8)
    def AIMove(self, x, y, speed):
        if speed > self.AIMaxSpeed:
            speed = self.AIMaxSpeed
        a = hypot(x, y)
        tX, tY = speed * x / a, speed * y / a
        self.yourBatData[0] = [tX + self.yourBatData[2][0], tY + self.yourBatData[2][1]]
    def playSound(self, sound, positionX):
        channel = sound.play()
        right = positionX / self.screenSize[0]
        left = 1 - right
        if channel is not None:
            channel.set_volume(left, right)
if __name__ == '__main__':
    I = Game()
    I.createWindow((1280, 490))
    I.setTitle("Hello")
    I.run(0.005)
