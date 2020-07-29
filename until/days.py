# encoding: utf-8

"""
操作days.json的方法
"""
import json

from WePro.basic import clockQuestionPath


class DaysRecord:
    def __init__(self):
        self.path = clockQuestionPath + '/' + 'days.json'
        with open(self.path, "r") as fp:
            self.data = json.load(fp)

    @property
    def days(self):
        return list(self.data['days'].keys())

    def add(self, date, fmt):
        newDay = {
            date.toString(): fmt
        }
        self.data['days'].update(newDay)

    def save(self):
        with open(self.path, "w") as fp:
            json.dump(self.data, fp, indent=2)

    def check(self, date):
        if date.toString in self.data['days']:
            return True
        return False

    def getFormat(self, date):
        if self.check(date):
            return self.data['days'][date.toString()]
        return None
