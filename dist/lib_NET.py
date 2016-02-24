#coding=utf-8
import time, socket, ori_Net
class Net(ori_Net.Net):
    """
    docstring for Net
    """

    def __init__(self):
        """
        docstring for __init__
        """
        super(Net, self).__init__()

    def getClientData(self, setting, data):
        """
        docstring for getClientData
        """
        msg = self.recvMsg()
        # print("Server recv data:%s" % str(msg))
        yourX, yourY = msg.split("|")
        return [setting["ScreenSize"][0] - float(yourX), float(yourY)]

    def sendServerData(self, data):
        """
        docstring for sendServerData
        """
        newData = "%s|%s|%s|%s|%s|%s" % (data["ball"]["pos"][0], data["ball"]["pos"][1], data["myBat"]["pos"][0], data["myBat"]["pos"][1], data["myScore"], data["yourScore"])
        # print("Server send data:%s" % str(newData))
        self.sendMsg(newData)

    def getServerData(self, setting, data):
        """
        docstring for getServerData
        """
        msg = self.recvMsg()
        # print("Client recv data:%s" % str(msg))
        ballX, ballY, yourX, yourY, yourScore, myScore = msg.split("|")
        # !
        data["ball"]["pos"][0] = setting["ScreenSize"][0] - float(ballX)
        data["ball"]["pos"][1] = float(ballY)
        data["yourBat"]["pos"][0] = setting["ScreenSize"][0] - float(yourX)
        data["yourBat"]["pos"][1] = float(yourY)
        if myScore.isdigit() or yourScore.isdigit():
            data["myScore"] = int(myScore)
            data["yourScore"] = int(yourScore)
        else:
            data["myScore"] = myScore
            data["yourScore"] = yourScore
        return data

    def sendClientData(self, data):
        """
        docstring for sendClientData
        """
        newData = "%s|%s" % (data["myBat"]["pos"][0], data["myBat"]["pos"][1])
        # print("Client send data:%s" % str(newData))
        self.sendMsg(newData)
if __name__ == '__main__':
    S = Net()
    C = Net()
    S.startServer(50000)
    #time.sleep(1)
    C.connect(C.getMyIP(), 50000)
