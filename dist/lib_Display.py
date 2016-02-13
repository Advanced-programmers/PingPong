#coding=utf-8
import time
import pygame
from pygame.locals import *
class Display():
    isRunning = True
    mousePos = [0, 0]
    def __init__(self):
        super(Display, self).__init__()
        pygame.init()
        self.init()
    def init(self):
        pass
    def createWindow(self, size = (640, 480)):
        self.screenSize = size
        self.screen = pygame.display.set_mode(size, 0, 32)
    def setTitle(self, title):
        pygame.display.set_caption(title)
    def run(self, interval = 0.01):
        self.setup()
        while self.isRunning:
            self.doInput()
            self.main()
            pygame.display.update()
            time.sleep(interval)
    def setup(self):
        pass
    def main(self):
        pass
    def doInput(self):
        eventList = pygame.event.get()
        for each in eventList:
            if each.type == QUIT:
                #print("[INFO]Get window Close.")
                self.isRunning = False
                pass
            elif each.type == KEYDOWN:
                #print("[INFO]Get key %s is Down." % each.key)
                pass
            elif each.type == KEYUP:
                #print("[INFO]Get key %s is Up." % each.key)
                pass
            elif each.type == MOUSEMOTION:
                #print("[INFO]Get mouse is at %s." % str(each.pos))
                self.mousePos = each.pos
                pass
            elif each.type == MOUSEBUTTONDOWN:
                #print("[INFO]Get mouse %s is Down." % each.button)
                pass
            elif each.type == MOUSEBUTTONUP:
                #print("[INFO]Get mouse %s is Up." % each.button)
                self.doMouseButtonUp(each.button)
                pass
    def doMouseButtonUp(self, button):
        pass
if __name__ == '__main__':
    I = Display()
    I.createWindow()
    I.setTitle("Hello")
    I.run()
