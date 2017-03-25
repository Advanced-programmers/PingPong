# coding=utf-8
import os
import time
import pygame
import threading
import numpy as np
from pygame.locals import *


class Game:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    setting = {
        # 全局
        'ScreenSize': [1366, 768],
        'Title': 'Hello',
        'Gravity': np.array([0, 0.1]),
        'WinScore': 20,
        # 人工智能
        'AIMaxSpeed': 10,
        'AIHitDistance': 10,
        # 道具尺寸
        'BallSize': 10,
        'BatSize': [2, 80],
        # 动力学
        'BatDecayRate': np.array([0.8, 1]),
        'NetDecayRate': np.array([0.8, 1]),
        # 调试
        'Debug': False,
        'FPS': 60
    }
    data = {
        'mouse': np.array([0, 0]),
        'your_mouse': np.array([0, 0]),
        'ball': {
            'speed': np.array([0, 0]),
            'pos': np.array([0, 0]),
            'las_pos': np.array([0, 0])
        },
        'my_bat': {
            'pos': np.array([0, 0]),
            'las_pos': np.array([0, 0]),
            'pdc_pos': np.array([0, 0])
        },
        'your_bat': {
            'pos': np.array([0, 0]),
            'las_pos': np.array([0, 0])
        },
        'my_score': 0,
        'your_score': 0,
        'ball_birth_point': np.array([0, 0]),
        'interval': setting['FPS']
    }
    flag = {
        'hitMyBat': False,
        'hitYourBat': False,
        'hitMyTable': False,
        'hitYourTable': False,
        'history': []
    }

    def __init__(self, debug=False):
        def fps_star():
            while self.isRunning['game']:
                time.sleep(1)
                self.data['fps'] = self.data['f']
                self.data['f'] = 0
                self.data['interval'] += self.setting['FPS'] - self.data['fps']
                if self.data['interval'] > 1000:
                    self.data['interval'] = 1000
                    self.setting['FPS'] -= 5

        self.isRunning = {}
        self.isRunning['game'] = True
        pygame.init()
        self.setting['NetSize'] = [2, self.setting['ScreenSize'][1] / 8]
        self.setting['TableSize'] = [self.setting['ScreenSize']
                                     [0] / 2, self.setting['ScreenSize'][1] / 16]
        if debug:
            self.setting['Debug'] = True
            self.data['f'] = 0
            self.data['fps'] = 0
            self.debug_font = pygame.font.Font('res\\Ubuntu-R.ttf', 14)

        os.system('title {}'.format(self.setting['Title']))
        os.system('cls')
        while True:
            self.setting['MyName'] = input('请输入玩家名字：')
            if self.setting['MyName'] == '':
                os.system('cls')
                print('不能为空！')
                print()
                continue
            elif len(self.setting['MyName']) > 10:
                os.system('cls')
                print('不能大于10！')
                print()
                continue
            break
        os.system('cls')
        while True:
            print('请输入模式(')
            print('输入“s”进入单人模式')
            print('输入“h”进入多人模式，并建立主机')
            print('输入“c”进入多人模式，并做客户端)')
            mode = input('：')
            if mode == 's' or mode == 'S':
                self.setting['Mode'] = 'SP'
                self.setting['YourName'] = 'Computer'
                self.data['your_f'] = np.array([0, 0])
                self.data['your_v'] = np.array([0, 0])
                break
            elif mode == 'h' or mode == 'H':
                pass
            elif mode == 'c' or mode == 'C':
                pass
            os.system('cls')
            print('必须选择一个模式！')
            print()
        self.font = pygame.font.Font('res\\Ubuntu-R.ttf', 32)
        self.screen = pygame.display.set_mode(
            self.setting['ScreenSize'], 0, 32)
        pygame.display.set_caption(self.setting['Title'])

        self.ball = pygame.Surface(
            (self.setting['BallSize'] * 2, self.setting['BallSize'] * 2))
        self.ball.fill(self.WHITE)
        pygame.draw.circle(self.ball, self.RED, [self.setting['BallSize'], self.setting['BallSize']],
                           self.setting['BallSize'])

        self.bat = pygame.Surface(self.setting['BatSize'])
        self.bat.fill(self.BLACK)

        self.net = pygame.Surface(self.setting['NetSize'])
        self.net.fill(self.BLACK)

        self.table = pygame.Surface(self.setting['TableSize'])
        self.net.fill(self.BLACK)
        # pygame.draw.rect(self.table, self.WHITE,
        # pygame.locals.Rect((2, 2), (self.setting['TableSize'][0] - 4,
        # self.setting['TableSize'][1] - 2)))

        # pygame.mouse.set_visible(False)

        t_fps = threading.Thread(target=fps_star)
        t_fps.start()

        while self.isRunning['game']:
            if self.setting['Debug']:
                self.data['f'] += 1
            self.doInput()
            self.update()
            self.doMain()
            pygame.display.update()
            time.sleep(1 / self.data['interval'])

            # if self.setting['Debug']:
            #     t_fps.join()

    def doInput(self):
        eventList = pygame.event.get()
        for each in eventList:
            if each.type == QUIT:
                # print('[INFO]Get window Close.')
                self.isRunning['game'] = False
                pass
            elif each.type == KEYDOWN:
                # print('[INFO]Get key %s is Down.' % each.key)
                pass
            elif each.type == KEYUP:
                # print('[INFO]Get key %s is Up.' % each.key)
                pass
            elif each.type == MOUSEMOTION:
                # print('[INFO]Get mouse is at %s.' % str(each.pos))
                # self.mousePos = [each.pos[0], each.pos[1]]
                self.data['mouse'] = np.array([each.pos[0], each.pos[1]])
                pass
            elif each.type == MOUSEBUTTONDOWN:
                # print('[INFO]Get mouse %s is Down.' % each.button)
                self.doAStart()
                pass
            elif each.type == MOUSEBUTTONUP:
                # print('[INFO]Get mouse %s is Up.' % each.button)
                pass

    def update(self):
        # self.data['your_mouse'] = self.doAI()
        # self.data['your_f'] = self.doAI()
        # tmp = np.sqrt(self.data['your_f'].dot(self.data['your_f']))
        # if tmp > 1:
        #     self.data['your_f'] = self.data['your_f'] / tmp
        #     self.data['your_v'] = np.add(self.data['your_v'], self.data['your_f'], casting='unsafe')
        # self.data['your_mouse'] = np.add(self.data['your_mouse'], self.data['your_v'], casting='unsafe')
        self.data['your_mouse'] = self.doAI()
        self.doLogic()

    def doAI(self):
        # if self.data['ball']['pos'][0] <= self.setting['ScreenSize'][0] / 2 and self.data['ball']['speed'][0] >= 0:
        #     # 返回
        #     return self.AIMoveTo(self.data['yourBat']['pos'][0], self.data['yourBat']['pos'][1], 64)
        # elif self.data['ball']['pos'][0] >= self.setting['ScreenSize'][0] / 2 and self.data['ball']['speed'][0] >= 0:
        #     # 恢复
        #     return self.AIMoveTo(self.setting['ScreenSize'][0] / 3,
        #                          (self.setting['ScreenSize'][1] / 2 + self.data['ball']['pos'][1]) / 2, 32)
        # elif self.data['ball']['pos'][0] >= self.setting['ScreenSize'][0] / 2 and self.data['ball']['speed'][0] <= 0:
        #     # 准备
        #     return self.AIMoveTo(self.setting['ScreenSize'][0] / 3, self.data['ball']['pos'][1], 32)
        # el
        def get_delta():
            d = self.data['ball']['pos'] - self.data['your_bat']['pos']
            delta = np.sqrt(d.dot(d))
            return [d[0], d[1], delta]

        def move_to(point, rate):
            delta = point - self.data['your_bat']['pos']
            delta = delta / rate
            return self.data['your_bat']['pos'] + delta

        if self.data['ball']['pos'][0] <= self.setting['ScreenSize'][0] / 8 and self.data['ball']['speed'][0] <= 0:
            # 击打
            if get_delta()[2] <= self.setting['AIHitDistance']:
                target = self.data['ball']['pos'] + \
                    np.array([self.setting['AIHitDistance'], 0])
                return move_to(target, 1)
            else:
                target = self.data['ball']['pos'] + np.array(
                    [-self.setting['AIHitDistance'], self.data['ball']['speed'][1]])
                return move_to(target, 8)
        elif self.data['ball']['pos'][0] <= self.setting['ScreenSize'][0] / 2 and self.data['ball']['speed'][0] <= 0:
            # 击打
            if get_delta()[2] <= self.setting['AIHitDistance']:
                target = self.data['ball']['pos'] + \
                    np.array([self.setting['AIHitDistance'], 0])
                return move_to(target, 1)
            else:
                target = self.data['ball']['pos'] + np.array(
                    [- self.setting['BallSize'] - self.setting['AIHitDistance'] + self.data['ball']['speed'][0] * 10,
                     self.data['ball']['speed'][1] * 10])
                return move_to(target, 8)
        return self.data['your_bat']['pos']

    def doLogic(self):
        # 我板
        self.data['my_bat']['las_pos'] = self.data['my_bat']['pos']
        self.data['my_bat']['pos'] = self.data['mouse']
        self.data['my_bat']['pdc_pos'] = self.data['my_bat']['pos'] - self.data['my_bat']['las_pos'] + \
            self.data['my_bat']['pos']
        if self.data['my_bat']['pos'][0] < self.setting['ScreenSize'][0] / 2 + self.setting['BatSize'][0] / 2:
            self.data['my_bat']['pos'][0] = self.setting[
                'ScreenSize'][0] / 2 + self.setting['BatSize'][0] / 2
            self.data['my_bat']['pdc_pos'][0] = self.data['my_bat']['pos'][0]
        # 你板
        self.data['your_bat']['las_pos'] = self.data['your_bat']['pos']
        self.data['your_bat']['pos'] = self.data['your_mouse']
        if self.data['your_bat']['pos'][0] > self.setting['ScreenSize'][0] / 2 + self.setting['BatSize'][0] / 2:
            self.data['your_bat']['pos'][0] = self.setting[
                'ScreenSize'][0] / 2 - self.setting['BatSize'][0] / 2
        # 球的物理
        self.data['ball']['speed'] = np.add(self.data['ball']['speed'], self.setting[
                                            'Gravity'], casting='unsafe')
        self.data['ball']['pos'] = np.add(self.data['ball']['pos'], self.data[
                                          'ball']['speed'], casting='unsafe')
        # 碰撞地板
        if self.data['ball']['pos'][1] + self.setting['BallSize'] > self.setting['ScreenSize'][1]:
            self.data['ball']['pos'][1] = self.setting[
                'ScreenSize'][1] - self.setting['BallSize']
            self.data['ball']['speed'][1] = - \
                abs(self.data['ball']['speed'][1]) * 0.9
            if self.data['ball']['pos'][0] > self.setting['ScreenSize'][0] / 2:
                self.judge('hitRightBad')
            else:
                self.judge('hitLeftBad')
        '''
        # 碰撞天花板
        if self.data['ball']['pos'][1] - self.setting['BallSize'] < 0:
            self.data['ball']['pos'][1] = self.setting['BallSize']
            self.data['ball']['speed'][1] = abs(self.data['ball']['speed'][1]) * 0.9
        '''
        # 碰撞桌面
        if (self.data['ball']['pos'][1] + self.setting['BallSize'] > self.setting['ScreenSize'][1] -
            self.setting['TableSize'][1]
            and self.data['ball']['pos'][0] + self.setting['BallSize'] > self.setting['ScreenSize'][0] / 2 -
            self.setting['TableSize'][
            0] / 2
            and self.data['ball']['pos'][0] - self.setting['BallSize'] < self.setting['ScreenSize'][0] / 2 +
            self.setting['TableSize'][
                0] / 2):
            self.data['ball']['pos'][1] = self.setting['ScreenSize'][1] - self.setting['TableSize'][1] - self.setting[
                'BallSize']
            self.data['ball']['speed'][1] = - \
                abs(self.data['ball']['speed'][1]) * 0.9
            if self.data['ball']['pos'][0] > self.setting['ScreenSize'][0] / 2:
                self.judge('hitRightTable')
            else:
                self.judge('hitLeftTable')
        # 碰撞左桌沿
        if (self.data['ball']['pos'][0] + self.setting['BallSize'] > self.setting['ScreenSize'][0] / 2 -
                self.setting['TableSize'][0] / 2
            and self.data['ball']['pos'][1] + self.setting['BallSize'] > self.setting['ScreenSize'][1] -
                self.setting['TableSize'][1]
                and self.data['ball']['pos'][0] < self.setting['ScreenSize'][0] / 2):
            self.data['ball']['pos'][0] = self.setting['ScreenSize'][0] / 2 - self.setting['TableSize'][0] / 2 - \
                self.setting['BallSize']
            self.data['ball']['speed'][0] = - \
                abs(self.data['ball']['speed'][0]) * 0.9
            self.judge('hitLeftBad')
        # 碰撞右桌沿
        if (self.data['ball']['pos'][0] - self.setting['BallSize'] < self.setting['ScreenSize'][0] / 2 +
                self.setting['TableSize'][0] / 2
            and self.data['ball']['pos'][1] + self.setting['BallSize'] > self.setting['ScreenSize'][1] -
                self.setting['TableSize'][1]
                and self.data['ball']['pos'][0] > self.setting['ScreenSize'][0] / 2):
            self.data['ball']['pos'][0] = self.setting['ScreenSize'][0] / 2 + self.setting['TableSize'][0] / 2 + \
                self.setting['BallSize']
            self.data['ball']['speed'][0] = abs(
                self.data['ball']['speed'][0]) * 0.9
            self.judge('hitRightBad')
        # 碰撞右墙
        if self.data['ball']['pos'][0] + self.setting['BallSize'] > self.setting['ScreenSize'][0]:
            self.data['ball']['pos'][0] = self.setting[
                'ScreenSize'][0] - self.setting['BallSize']
            self.data['ball']['speed'][0] = - \
                abs(self.data['ball']['speed'][0]) * 0.9
            self.judge('hitRightBad')
            if isinstance(self.data['your_score'], str) or isinstance(self.data['your_score'], str):
                self.data['your_score'], self.data['my_score'] = 0, 0
            self.data['your_score'] += 1
        # 碰撞左墙
        if self.data['ball']['pos'][0] - self.setting['BallSize'] < 0:
            self.data['ball']['pos'][0] = self.setting['BallSize']
            self.data['ball']['speed'][0] = abs(
                self.data['ball']['speed'][0]) * 0.9
            self.judge('hitLeftBad')
            if isinstance(self.data['your_score'], str) or isinstance(self.data['your_score'], str):
                self.data['your_score'], self.data['my_score'] = 0, 0
            self.data['my_score'] += 1
        # 球碰撞我板
        if (self.data['ball']['pos'][0] > self.data['my_bat']['pos'][0] - self.setting['BallSize'] -
                self.setting['BatSize'][0] / 2
            and self.data['ball']['pos'][0] < self.data['my_bat']['pos'][0] + self.setting['BallSize'] +
            self.setting['BatSize'][0] / 2
            and self.data['ball']['pos'][1] > self.data['my_bat']['pos'][1] - self.setting['BallSize'] -
            self.setting['BatSize'][1] / 2
            and self.data['ball']['pos'][1] < self.data['my_bat']['pos'][1] + self.setting['BallSize'] +
                self.setting['BatSize'][1] / 2):
            self.judge('hitRightBat')
            self.data['ball']['pos'][0] = self.data['my_bat']['pos'][0] - self.setting['BallSize'] - \
                self.setting['BatSize'][0] / 2
            self.data['ball']['speed'][0] = (self.data['my_bat']['pos'][0] - self.data['my_bat']['las_pos'][0] -
                                             self.data['ball']['speed'][
                                                 0]) * self.setting['BatDecayRate'][0]
            self.data['ball']['speed'][1] = (self.data['my_bat']['pos'][1] - self.data['my_bat']['las_pos'][1] +
                                             self.data['ball']['speed'][
                                                 1]) * self.setting['BatDecayRate'][1]
        # 球碰撞你板
        if (self.data['ball']['pos'][0] > self.data['your_bat']['pos'][0] - self.setting['BallSize'] -
                self.setting['BatSize'][0] / 2
            and self.data['ball']['pos'][0] < self.data['your_bat']['pos'][0] + self.setting['BallSize'] +
            self.setting['BatSize'][0] / 2
            and self.data['ball']['pos'][1] > self.data['your_bat']['pos'][1] - self.setting['BallSize'] -
            self.setting['BatSize'][1] / 2
            and self.data['ball']['pos'][1] < self.data['your_bat']['pos'][1] + self.setting['BallSize'] +
                self.setting['BatSize'][1] / 2):
            self.judge('hitLeftBat')
            self.data['ball']['pos'][0] = self.data['your_bat']['pos'][0] + self.setting['BallSize'] + \
                self.setting['BatSize'][0] / 2
            self.data['ball']['speed'][0] = (self.data['your_bat']['pos'][0] - self.data['your_bat']['las_pos'][0] -
                                             self.data['ball']['speed'][0]) * self.setting['BatDecayRate'][0]
            self.data['ball']['speed'][1] = (self.data['your_bat']['pos'][1] - self.data['your_bat']['las_pos'][1] +
                                             self.data['ball']['speed'][1]) * self.setting['BatDecayRate'][1]
        # 球碰撞网
        if (self.data['ball']['pos'][0] > self.setting['ScreenSize'][0] / 2 - self.setting['NetSize'][0] / 2 -
            self.setting['BallSize']
            and self.data['ball']['pos'][0] < self.setting['ScreenSize'][0] / 2 + self.setting['NetSize'][0] / 2 +
                self.setting['BallSize']
            and self.data['ball']['pos'][1] > self.setting['ScreenSize'][1] - self.setting['TableSize'][1] -
                self.setting['NetSize'][1] -
                self.setting['BallSize']):
            if self.data['ball']['speed'][0] > 0:
                self.data['ball']['pos'][0] = self.setting['ScreenSize'][0] / 2 - self.setting['NetSize'][0] / 2 - \
                    self.setting['BallSize']
                self.data['ball']['speed'][0] = - self.data['ball']['speed'][0]
            elif self.data['ball']['speed'][0] < 0:
                self.data['ball']['pos'][0] = self.setting['ScreenSize'][0] / 2 + self.setting['NetSize'][0] / 2 + \
                    self.setting['BallSize']
                self.data['ball']['speed'][0] = - self.data['ball']['speed'][0]
            elif self.data['ball']['speed'][0] == 0:
                self.data['ball']['pos'][1] = self.setting['ScreenSize'][1] - self.setting['TableSize'][1] - \
                    self.setting['NetSize'][1] - \
                    self.setting['BallSize']
                self.data['ball']['speed'][1] = - self.data['ball']['speed'][1]
            self.judge('hitNet')
        if isinstance(self.data['your_score'], int) and isinstance(self.data['your_score'], int) and (
            self.data['your_score'] >= self.setting['WinScore'] or self.data['my_score'] >= self.setting[
                'WinScore']):
            if self.data['my_score'] >= self.setting['WinScore']:
                self.data['your_score'], self.data['my_score'] = 'Lose', 'Win'
            else:
                self.data['your_score'], self.data['my_score'] = 'Win', 'Lose'
            time.sleep(1)
            data = self.doAStart()

    def judge(self, event):
        # TODO
        print(event)
        if event == 'hitRightBat':
            if self.flag['hitMyTable'] is True:  #
                self.flag['hitMyTable'] = False
            else:
                self.youGet()
        elif event == 'hitLeftBat':
            if self.flag['hitYourTable'] is True:  #
                self.flag['hitYourTable'] = False
            else:
                self.iGet()
        elif event == 'hitLeftTable':
            if self.flag['hitYourTable'] is True:  # hit your ground twice.
                self.iGet()
        elif event == 'hitRightGround':
            if self.flag['hitMyTable'] is True:  # hit my ground twice.
                self.youGet()
            else:
                self.flag['hitMyTable'] = True
                self.flag['hitYourBat'] = False
        elif event == 'hitRightBad':
            if self.flag['hitMyTable'] is True:
                self.youGet()
            else:
                self.iGet()
        elif event == 'hitLeftBad':
            if self.flag['hitYourTable'] is True:
                self.iGet()
            else:
                self.youGet()
        elif event == 'hitNet':
            if self.flag['hitMyBat'] is True:
                self.youGet()
            elif self.flag['hitYourBat'] is True:
                self.iGet()
            else:
                print('[WARN]Cannot judge.')
        self.flag['history'].append(event)

    def iGet(self):
        '''
        docstring for Iget
        '''
        print('IWin')
        self.flag['hitMyTable'] = False
        self.flag['hitYourTable'] = False
        self.flag['hitMyBat'] = False
        self.flag['hitYourBat'] = False

    def youGet(self):
        '''
        docstring for youGet
        '''
        print('youWin')
        self.flag['hitMyTable'] = False
        self.flag['hitYourTable'] = False
        self.flag['hitMyBat'] = False
        self.flag['hitYourBat'] = False

    def doAStart(self, ):
        '''
        docstring for doAStart
        '''
        self.data['ball']['pos'] = [self.setting['ScreenSize'][0] / 4 * 3, 100]
        self.data['ball']['speed'] = [0, 0]
        self.data['ball']['las_pos'] = [0, 0]

    def doMain(self):
        self.screen.fill(self.WHITE)

        # 绘制
        score = self.font.render('{} : {}'.format(self.data['your_score'], self.data['my_score']), True, self.BLACK,
                                 self.WHITE)
        self.screen.blit(self.table, (self.setting['ScreenSize'][0] / 2 - self.setting['TableSize'][0] / 2,
                                      self.setting['ScreenSize'][1] - self.setting['TableSize'][1]))
        self.screen.blit(self.net, (self.setting['ScreenSize'][0] / 2 - self.setting['NetSize'][0] / 2,
                                    self.setting['ScreenSize'][1] - self.setting['NetSize'][1] -
                                    self.setting['TableSize'][1]))
        pos = (self.data['ball'][
               'pos'] - np.array([self.setting['BallSize'], self.setting['BallSize']]))
        self.screen.blit(self.ball, pos)
        pos = (
            self.data['my_bat']['pdc_pos'] - np.array([self.setting['BatSize'][0] / 2, self.setting['BatSize'][1] / 2]))
        self.screen.blit(self.bat, pos)
        pos = (
            self.data['your_bat']['pos'] - np.array([self.setting['BatSize'][0] / 2, self.setting['BatSize'][1] / 2]))
        self.screen.blit(self.bat, pos)
        self.screen.blit(score, (self.setting['ScreenSize'][
                         0] / 2 - score.get_width() / 2, 0))
        if self.setting['Debug']:
            fps = self.debug_font.render('fps: {} interval: {}'.format(self.data['fps'], self.data['interval']), True,
                                         self.BLACK, self.WHITE)
            self.screen.blit(fps, (0, 0))


if __name__ == '__main__':
    A = Game(True)
