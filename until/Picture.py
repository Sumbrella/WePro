import os


class Picture:
    def __init__(self, file, size=0):
        self.size = size
        self.file = file
        self.format = os.path.splitext(file.filename)[1][1:]

    @staticmethod
    def fromRequest(request):
        file = request.files.get("file")
        fileSize = int(request.form.get("size"))

        return Picture(file, fileSize)

    def save(self, path):
        self.file.save(path, self.size + 10)
