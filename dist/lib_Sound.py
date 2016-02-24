# coding=utf-8
import pygame


class Sound(object):
    """
    docstring for Sound
    """


    def __init__(self):
        """
        docstring for __init__
        """
        super(Sound, self).__init__()
        pygame.init()

        self.sound_ping = pygame.mixer.Sound("res\\ping.wav")
        self.sound_pong = pygame.mixer.Sound("res\\pong.wav")
        self.sound_a = pygame.mixer.Sound("res\\a.wav")
        self.sound_wu = pygame.mixer.Sound("res\\wu.wav")
        self.sound_ha = pygame.mixer.Sound("res\\ha.wav")

    def playSound(self, setting, sound, positionX):
        channel = sound.play()
        right = positionX / setting["ScreenSize"][0]
        left = 1 - right
        if channel is not None:
            channel.set_volume(left, right)
if __name__ == '__main__':
    I = Sound()
