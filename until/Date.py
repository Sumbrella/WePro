"""

"""
import json, os
from WePro import basic
from WePro.until.days import DaysRecord


class Date:
    def __init__(self, year, month, day, code=None):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)

        if code:
            self.code = int(code)
        else:
            self.code = self.getCheckCode()

    @staticmethod
    def fromJson(js):
        date_dict = json.loads(js)
        return Date(date_dict['year'], date_dict['month'], date_dict['day'])

    @staticmethod
    def fromRequest(request):
        if request.form:
            date = request.form.get("date")
        else:
            date = request.args.get("date")
        if not date:
            print("can't get date in Date.py")
            raise

        return Date.fromJson(date)

    @staticmethod
    def fromLocalDate(date):
        """
        :param date: String [2020-10-10-{checkcode}]
        :return:
        """
        year, month, day, code = date.split('-')
        return Date(year, month, day, code)

    def toString(self):
        return "{}{:02d}{:02d}".format(self.year, self.month, self.day)

    def getCheckCode(self):
        _sum = 0
        _sum += self.year * 2 + self.month * 4 + self.year * 8

        return _sum % 10

    def checkCode(self):
        targetCode = self.getCheckCode()
        if targetCode == self.code:
            return True
        else:
            return False

    def getQuestionPath(self, fmt):
        if fmt is None:
            daysRecord = DaysRecord()
            fmt = daysRecord.getFormat(self)
            if fmt is None:
                fmt = "jpg"

        questionPath = basic.clockQuestionPath
        fileName = self.toString() + "." + fmt
        targetPath = os.path.join(questionPath, fileName)

        return targetPath
