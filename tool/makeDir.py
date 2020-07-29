import os


def makeDir(dirPath):
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
