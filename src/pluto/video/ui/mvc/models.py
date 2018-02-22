import os


class Task(object):
    def __init__(self):
        self.filename = ""
        self.file = ""
        self.folder = ""
        self.subtitle = ""
        self.start = 0
        self.end = 0
        self.output = ""
        self.isPlaying = False
        self.task_progress = 0

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == 'filename' and value != "":
            self.folder, self.file = os.path.split(value)
            if self.__dict__['output'] == "":
                self.__dict__['output'] = self.folder
