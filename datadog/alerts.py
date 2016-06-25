"""The alerts module collects and processes alerts"""

from collections import Counter, deque, namedtuple
from datetime import datetime as dt
import threading

from parser import parse_line

AlertsEntry = namedtuple('AlertsEntry', ['timestamp', 'logentry'])

def process_alerts(alerts_data, duration=120, threshold=200):
    """Processes alerts on the given alerts data
    Args:
        alerts_data (LogAlertsQueue): a list of log lines and timestamps
        duration (int): length of time in sec till which we will consider data
        threshold (int): traffic threshold in bytes
        fd (file handle): a file handle to write alerts data to"""
    thread = threading.Timer(duration, process_alerts, [alerts_data, duration, threshold])
    # make sure all threads exit on ctrl+c
    thread.daemon = True
    thread.start()
    if len(alerts_data) > 0:
        alerts_data.purge(duration)
        current_sum = 0
        for entry in alerts_data:
            current_sum += entry.logentry.length
        try:
            avg = float(current_sum) / len(alerts_data)
        except ZeroDivisionError:
            avg = 0
        if avg >= threshold:
            msg = "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=avg, time=dt.now())
        else:
            msg = "Traffic went below threshold {threshold} at {time}".format(threshold=threshold, time=dt.now())
        print "\n" + msg

class LogAlertsQueue(deque):
    """Represents a deque with tuples of type AlertsEntry"""
    def __init__(self):
        super(LogAlertsQueue, self).__init__()
        self.traffic_counter = Counter()

    def add(self, logentry):
        """Adds a logentry to the deque"""
        self.traffic_counter[logentry.section] += logentry.length
        self.append(AlertsEntry(dt.now(), logentry))

    def purge(self, duration):
        """Purges all data which were added before duration"""
        now = dt.now()
        while len(self) != 0 and (now - self[0].timestamp).seconds > duration:
            oldest = self.popleft()
            self.traffic_counter[oldest.logentry.section] -= oldest.logentry.length

    def __str__(self):
        for item in self:
            return str(item.timestamp) + " " + str(item.logentry)
