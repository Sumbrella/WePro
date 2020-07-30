import os
import csv

from WePro.basic import clockQuestionPath


def saveClockDescription(fileLock, user, date, fmt):
    """
    Save the clock record into csv file
    row: [date, openid, studentNo, grade, college, format ]
    """
    fileLock.acquire()

    descriptionPath = os.path.join(clockQuestionPath, "description", "description.csv")
    schoolInfo = user.getSchoolInfo()

    dataRow = [date.toString(), user.openid, schoolInfo.studentNo, schoolInfo.grade, schoolInfo.college, fmt]
    with open(descriptionPath, "a+", encoding="utf-8") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(dataRow)

    fileLock.release()
