""""""
import os
import time
import json

from WePro.tool.makeDir import makeDir
from WePro.until.Date import Date
from WePro.basic import usersPath
from WePro import routes


class User:
    def __init__(self, openid):
        self._openid = openid
        self._userDir = os.path.join(usersPath, openid)
        self._schoolInfoPath = os.path.join(self.userDir, "schoolInfo.json")

        self.makeUserDir()
        # self.makeUserInfoFile()

    @staticmethod
    def fromRequest(request):
        if request.form:
            return User(request.form.get("openid"))
        else:
            return User(request.args.get("openid"))

    @property
    def userDir(self):
        return self._userDir

    @property
    def openid(self):
        return self._openid

    def makeUserDir(self):
        # make special dir
        try:
            userPath = os.path.join(usersPath, self.openid)
            makeDir(userPath)
            makeDir(os.path.join(userPath, routes.clockPicture))
        except Exception as e:
            print("[ERROR] In User.py make user's special dir:", e)
            raise e

    def getClockPicturePath(self, pictureDate, pictureFormat):
        """
        :param pictureDate: the date picture uploaded
        :param pictureFormat: String like ".jpg"
        :return: the path of picture need to be saved
        """
        pathName = os.path.join(self.userDir, "clockPicture", pictureDate.toString())

        return pathName + "." + pictureFormat

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

    def getSchoolInfo(self):
        with open(self._schoolInfoPath, "r") as fp:
            data = json.load(fp)
            return data

    def saveSchoolInfo(self, schoolInfo):
        with open(self._schoolInfoPath, "w") as fp:
            json.dump(schoolInfo, fp)

