""""""
import os, time

from ..tool.makeDir import makeDir
from .Date import Date
from ..basic import usersPath
from WePro import routes


class User:
    def __init__(self, openid):
        self.openid = openid
        self.userDir = os.path.join(usersPath, openid)

        self.makeUserDir()
        # self.makeUserInfoFile()

    @staticmethod
    def fromRequest(request):
        if request.form:
            return User(request.form.get("openid"))
        else:
            return User(request.args.get("openid"))

    def makeUserDir(self):
        # make special dir
        try:
            userPath = os.path.join(usersPath, self.openid)
            makeDir(userPath)
            makeDir(os.path.join(userPath, routes.clockPicture))
        except Exception as e:
            print("[ERROR] In User.py make user's special dir:", e)
            raise e

    def makeUserInfoFile(self):
        # TODO: make a userInfo file
        return

    def getClockPicturePath(self, pictureDate, pictureFormat):
        """
        :param pictureDate: the date picture uploaded
        :param pictureFormat: String like ".jpg"
        :return: the path of picture need to be saved
        """
        pathName = os.path.join(self.userDir, "clockPicture", pictureDate.toString())

        return pathName + pictureFormat

    def getSessionKey(self):
        t = time.localtime()
        today = Date(t.tm_year, t.tm_mon, t.tm_mday)
        # for each character in openid
        sessionKey = ""
        for c in self.openid:
            asc = ord(c)
            sessionKey += chr((asc+1) * 2 % 128)
        sessionKey += chr(today.getCheckCode())

        return sessionKey

    def checkSessionKey(self, key):
        sessionKey = self.getSessionKey()

        for i in range(len(key)):
            if key[i] != sessionKey[i]:
                return False
        return True
