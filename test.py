from WePro.until.days import DaysRecord
from WePro.until.Date import Date

dr = DaysRecord()
dt = Date(2020, 7, 31)
dr.add(dt, 'jpg')
dr.save()
