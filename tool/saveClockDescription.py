import os
import csv

from WePro.basic import clockQuestionPath


def saveClockDescription(fileLock, user, clockDate, submitDate, fmt):
    """
    Save the clock record into csv file
    row: openid, clockDate, submitDate, format,
    """
    fileLock.acquire()

    descriptionPath = os.path.join(clockQuestionPath, "description", "description.csv")

    dataRow = [user.openid, clockDate.toString(), submitDate.toString(), fmt]
    with open(descriptionPath, "a+", encoding="utf-8") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(dataRow)

    fileLock.release()
