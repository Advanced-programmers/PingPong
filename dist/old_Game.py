#coding=utf-8
import pygame, random, time
from math import *
from pygame.locals import *
import lib_Display, lib_Net, lib_AI, lib_Sound


class Game(lib_Display.Display):
    """docstring for Game"""
    def __init__(self):
        super(Game, self).__init__()
    def init(self):
        self.batDecayRate = [0.8, 1]
        self.Gravity = 0.05
        self.yourScore, self.myScore = 0, 0
        self.AIMaxSpeed = 20
        self.AIHitDistance = 10
        self.winScore = 20
        self.ai = lib_AI.AI()
        self.Net = lib_Net.Net()
        self.sound = lib_Sound.Sound()
        self.mode = input('请输入模式(\n输入“s”进入单人模式\n输入“h”进入多人模式，并建立主机\n输入“c”进入多人模式，并做客户端)\n：')
        if self.mode == "s":
            pass
        elif self.mode == "h":
            print("本机IP：%s" % self.Net.getMyIP())
            port = input("请输入端口号(默认50000)：")
            if port == "":
                port = "50000"
            self.Net.startServer(int(port))
        elif self.mode == "c":
            print("本机IP：%s" % self.Net.getMyIP())
            host = input("请输入IP(默认本机IP)：")
            if host == "":
                host = self.Net.getMyIP()
            port = input("请输入端口号(默认50000)：")
            if port == "":
                port = "50000"
            self.Net.connect(host, int(port))
    def setup(self):
        pygame.mouse.set_visible(False)

        setting = {}
        setting["ScreenSize"] = self.screenSize
        self.sound.init(setting)

        if self.mode == "s":
            self.setTitle("SinglePlayer (Press right mouse button to reset ball.)")
        elif self.mode == "ms":
            self.setTitle("Server (Press right mouse button to reset ball.)")
        elif self.mode == "mc":
            self.setTitle("Client (Press right mouse button to reset ball.)")

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
            self.font = pygame.font.Font("res\\Ubuntu-R.ttf", 32)
        except OSError as e:
            print("[WARN]" + str(e))
            print("[    ]Game.Game.setup()")
            print("[    ]self.font = pygame.font.Font('Ubuntu-R.ttf', 32)")
        finally:
            pass
        if self.mode == "ms":
            newData = "%s|%s|%s|%s|%s|%s" % (self.ballData[0][0], self.ballData[0][1], self.myBatData[0][0], self.myBatData[0][1], self.myScore, self.yourScore)
            print("Server send data:%s"%str(newData))
            self.Net.sendMsg(newData)
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
            setting = {}
            setting["AIHitDistance"] = self.AIHitDistance
            setting["AIMaxSpeed"] = self.AIMaxSpeed
            setting["BallSize"] = self.ballData[1]
            setting["screenSize"] = self.screenSize
            data = {}
            data["ball"] = {}
            data["ball"]["pos"] = self.ballData[0]
            data["ball"]["lastPos"] = self.ballData[2]
            data["yourBat"] = {}
            data["yourBat"]["pos"] = self.yourBatData[0]
            data["yourBat"]["lastPos"] = self.yourBatData[2]
            self.yourBatData[0] = self.ai.doAI(setting, data)
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
                self.sound.playSound(self.sound.sound_pong, self.ballData[0][0])
            # 碰撞天花板
            if self.ballData[0][1] - self.ballData[1] < 0:
                self.ballData[0][1] = self.ballData[1]
                self.ballData[2][1] = abs(self.ballData[2][1]) * 0.9
                self.sound.playSound(self.sound.sound_pong, self.ballData[0][0])
            # 碰撞右墙
            if self.ballData[0][0] + self.ballData[1] > self.screenSize[0]:
                self.ballData[0][0] = self.screenSize[0] - self.ballData[1]
                self.ballData[2][0] = -abs(self.ballData[2][0]) * 0.9
                self.sound.playSound(self.sound.sound_pong, self.ballData[0][0])
                if isinstance(self.yourScore, str)  or isinstance(self.yourScore, str):
                    self.yourScore, self.myScore = 0, 0
                if self.yourScore - self.myScore >= 5:
                    self.sound.playSound(self.sound_a, self.screenSize[0])
                self.yourScore += 1
            # 碰撞左墙
            if self.ballData[0][0] - self.ballData[1] < 0:
                self.ballData[0][0] = self.ballData[1]
                self.ballData[2][0] = abs(self.ballData[2][0]) * 0.9
                self.sound.playSound(self.sound.sound_pong, self.ballData[0][0])
                if isinstance(self.yourScore, str)  or isinstance(self.yourScore, str):
                    self.yourScore, self.myScore = 0, 0
                if self.myScore - self.yourScore >= 5:
                    self.sound.playSound(self.sound_a, 0)
                self.myScore += 1
            # 球碰撞我板
            if (self.ballData[0][0] > self.myBatData[0][0] - self.ballData[1] - self.myBatData[1][0] / 2
                and self.ballData[0][0] < self.myBatData[0][0] + self.ballData[1] + self.myBatData[1][0] / 2
                and self.ballData[0][1] > self.myBatData[0][1] - self.ballData[1] - self.myBatData[1][1] / 2
                and self.ballData[0][1] < self.myBatData[0][1] + self.ballData[1] + self.myBatData[1][1] / 2):
                self.sound.playSound(self.sound.sound_ping, self.ballData[0][0])
                self.ballData[0][0] = self.myBatData[0][0] - self.ballData[1] - self.myBatData[1][0] / 2
                self.ballData[2][0] = (self.myBatData[0][0] - self.myBatData[2][0] - self.ballData[2][0]) * self.batDecayRate[0]
                self.ballData[2][1] = (self.myBatData[0][1] - self.myBatData[2][1] + self.ballData[2][1]) * self.batDecayRate[1]
            # 球碰撞你板
            if (self.ballData[0][0] > self.yourBatData[0][0] - self.ballData[1] - self.yourBatData[1][0] / 2
                and self.ballData[0][0] < self.yourBatData[0][0] + self.ballData[1] + self.yourBatData[1][0] / 2
                and self.ballData[0][1] > self.yourBatData[0][1] - self.ballData[1] - self.yourBatData[1][1] / 2
                and self.ballData[0][1] < self.yourBatData[0][1] + self.ballData[1] + self.yourBatData[1][1] / 2):
                self.sound.playSound(self.sound.sound_ping, self.ballData[0][0])
                self.ballData[0][0] = self.yourBatData[0][0] + self.ballData[1] + self.yourBatData[1][0] / 2
                self.ballData[2][0] = (self.yourBatData[0][0] - self.yourBatData[2][0] - self.ballData[2][0]) * self.batDecayRate[0]
                self.ballData[2][1] = (self.yourBatData[0][1] - self.yourBatData[2][1] + self.ballData[2][1]) * self.batDecayRate[1]
            if isinstance(self.yourScore, int) and isinstance(self.yourScore, int) and (self.yourScore >= self.winScore or self.myScore >= self.winScore):
                if self.myScore >= self.winScore:
                    self.yourScore, self.myScore = "Lose", "Win"
                    self.sound.playSound(self.sound.sound_ha, self.screenSize[0])
                    time.sleep(1)
                    self.sound.playSound(self.sound.sound_wu, 0)
                else:
                    self.yourScore, self.myScore = "Win", "Lose"
                    self.sound.playSound(self.sound.sound_wu, self.screenSize[0])
                    time.sleep(1)
                    self.sound.playSound(self.sound.sound_ha, 0)
                self.ballData = [[self.screenSize[0] / 2, 100], 10, [0, 0]]
        elif self.mode == "ms":
            data = self.Net.recvMsg()
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
            self.Net.sendMsg(newData)
        elif self.mode == "mc":
            data = self.Net.recvMsg()
            print("Client recv data:%s"%str(data))
            ballX, ballY, yourX, yourY, yourScore, myScore = data.split("|")
            #
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
            self.Net.sendMsg(newData)
        #

        score = self.font.render("%s : %s" % (self.yourScore, self.myScore), True, (0,0,0), (255, 255, 255))
        self.screen.blit(self.ball, (self.ballData[0][0] - self.ballData[1], self.ballData[0][1] - self.ballData[1]))
        self.screen.blit(self.myBat, (self.myBatData[0][0] - self.myBatData[1][0] / 2, self.myBatData[0][1] - self.myBatData[1][1] / 2))
        self.screen.blit(self.yourBat, (self.yourBatData[0][0] - self.yourBatData[1][0] / 2, self.yourBatData[0][1] - self.yourBatData[1][1] / 2))
        self.screen.blit(score, (self.screenSize[0] / 2 - score.get_width() / 2, 0))
    def doMouseButtonUp(self, button):
        if button == 3:
            self.ballData = [[self.screenSize[0] / 2, 100], 10, [0, 0]]
if __name__ == '__main__':
    I = Game()
    I.createWindow((1280, 490))
    I.setTitle("Hello")
    I.run(0.005)
