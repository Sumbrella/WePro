# encoding: utf-8
import os

from flask import Flask, request, Response
from werkzeug.datastructures import FileStorage

from WePro import routes
from WePro import basic
from WePro.messages import *
from WePro.until.User import User
from WePro.until.Date import Date
from WePro.until.Picture import Picture


app = Flask(__name__)


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
    if date.checkCode():
        targetName = date.toString()
        questionFiles = os.listdir(basic.clockQuestionPath)
        for fileName in questionFiles:
            realName, extName = os.path.splitext(fileName)
            if realName == targetName:
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
    user = User.fromRequest(request)
    date = Date.fromRequest(request)
    picture = Picture.fromRequest(request)
    savedPath = date.getQuestionPath(picture.format)
    picture.save(savedPath)
    return PICTURE_RECEIVED


@app.route("/{}/".format(routes.checkTime), methods=['GET'])
def handleTimeSwap():
    date = Date.fromRequest(request)
    if not date.checkCode():
        return CODE_ERROR
    os.path.getmtime(date.getQuestionPath())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
