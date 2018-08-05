
class Logger(object):
    _instance = None

    def __init__(self):
        super(Logger, self).__init__()
        self.logs = {}

    def log(self, track, data):
        if track in self.logs:
            self.logs[track] += data
        else:
            self.logs[track] = data

    def clearTrack(self,track):
        self.logs[track] = ""

    def getTrack(self,track):
        return self.logs[track]

    def printTrack(self,track):
        print ("track " + track + ": " + self.logs[track])


    @staticmethod
    def getInstance():
        if not Logger._instance:
            Logger._instance = Logger()
        return Logger._instance
