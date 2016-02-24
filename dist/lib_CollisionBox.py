# coding=utf-8


class CollisionBox(object):
    """
    目前只支持以下碰撞检测：
        "object" 与 "object" 之间；
        "object" 与 "side", "sides" 之间。
    暂不支持：
        "side", "sides" 与 "side", "sides" 之间。
    """
    boxList = []

    def __init__(self):
        """
        docstring for __init__
        """
        super(CollisionBox, self).__init__()

    def addBox(self, position=[0, 0], size=[0, 0], type):
        """
        position:以矩形的左上角为准
        type:"object", "side", "sides"
        """
        pass

    def update(self):
        """
        docstring for update
        """
        pass


class CollisionBoxUnit(object):
    """docstring for CollisionBoxUnit"""

    def __init__(self):
        """
        docstring for __init__
        """
        super(CollisionBoxUnit, self).__init__()
if __name__ == '__main__':
    I = CollisionBox()
