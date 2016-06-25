"""Represents models used in the project"""

class LogEntry(object):
    """A log entry as read from the file"""
    def __init__(self, ip, time, request, status, size):
        self.ip = ip
        self.time = time
        self.request = request
        self.status = status
        self.size = size

    @property
    def section(self):
        """Returns the formatted section for the log entry"""
        uri = self.request.split(' ')[1]
        parts = uri.split('/')
        return parts[0] + "//" + parts[2] + '/' + parts[3]

    @property
    def length(self):
        """Returns the size of the entry in bytes, returns 0 if there
        is no value"""
        if self.size == '-':
            return 0
        return int(self.size)
