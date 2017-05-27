class LogginSystem(object):

    def __init__(self, file_location):
        self.log_file = open(file_location, 'a+')

    def write(self, message):
        self.log_file.write(message)

    def __del__(self):
        self.log_file.close()