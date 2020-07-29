# encoding: utf-8
import os

from flask import Flask, request, Response, current_app

from WePro import routes
from WePro import basic
from WePro.messages import *
from WePro.until.User import User
from WePro.until.Date import Date
from WePro.until.Picture import Picture
from WePro.until.days import DaysRecord
from WePro.until.Lock import Lock


app = Flask(__name__)
app.datesLock = Lock.getFileLock('dates')


@app.route("/")
def hello():
    return "<h1 style='color: red;'> ！！我最喜欢丹丹老师！！ </h1>"


@app.route("/{}/".format(routes.clockPicture), methods=['POST'])
def handleSubmitPicture():
    """
    submit the user's clock picture from request
    :return:
    """
    try:
        user = User.fromRequest(request)
        date = Date.fromRequest(request)
        picture = Picture.fromRequest(request)
        filePath = user.getClockPicturePath(date, picture.format)
        picture.save(filePath)

    except Exception as e:
        print("[ERROR] in app.route(routes.clockPicture): ", e)
        return SERVER_ERROR
    else:
        return PICTURE_RECEIVED


@app.route("/{}/".format(routes.checkQuestion), methods=['GET'])
def checkQuestion():
    date = Date.fromRequest(request)
    user = User.fromRequest(request)
    days = DaysRecord()
    if date.checkCode():
        if days.check(date):
            fileName = date.toString() + "." + days.getFormat(Date)
            return {
                "f": fileName,
                "s": user.getSessionKey()
            }
        return FIND_QUESTION_ERROR
    else:
        return CODE_ERROR


@app.route("/{}/<data>".format(routes.question), methods=['GET'])
def handleGetQuestion(data):
    # user get the clock question from the client,
    # send the target date question-picture to user

    openid, fileName, sessionKey = data.split('-')
    user = User(openid)
    if user.checkSessionKey(sessionKey):
        with open(os.path.join(basic.clockQuestionPath, fileName), 'rb') as img_f:
            ext = os.path.splitext(fileName)[1]
            image = img_f.read()
            response = Response(image, mimetype="image/{}".format(ext[1:]))
            return response
    else:
        return CODE_ERROR


@app.route("/{}/".format(routes.submitQuestion), methods=['POST'])
def handleSubmitQuestion():
    """
    The Manager submit one day's question
    :return:
    """
    current_app.datesLock.acquire()
    # user = User.fromRequest(request)
    date = Date.fromRequest(request)
    days = DaysRecord()
    picture = Picture.fromRequest(request)
    savePath = date.getQuestionPath(picture.format)
    picture.save(savePath)
    days.add(date, picture.format)
    days.save()
    current_app.datesLock.release()

    return PICTURE_RECEIVED


@app.route("/{}/".format(routes.checkTime), methods=['GET'])
def handleTimeSwap():
    date = Date.fromRequest(request)
    if not date.checkCode():
        return CODE_ERROR
    fileTime = os.path.getmtime(date.getQuestionPath())
    return fileTime


@app.route("/{}/".format(routes.getAllDays), methods=['GET'])
def handleGetAllDays():
    date = Date.fromRequest(request)
    days = DaysRecord()
    if not date.checkCode():
        return CODE_ERROR
    return "/".join(days.days)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
