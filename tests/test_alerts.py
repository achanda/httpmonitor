import unittest
import sys
import time

from StringIO import StringIO

from datadog.alerts import LogAlertsQueue, process_alerts
from datadog.parser import parse_line

class AlertsTest(unittest.TestCase):
    def setUp(self):
        logs = """pwpark.remote.Princeton.EDU - - [28/Aug/1995:00:01:50 -0400] "GET http://www.quora.com/pub/peace/VRS9.html HTTP/1.0" 200 2187
debasement.clark.net - - [28/Aug/1995:00:01:54 -0400] "GET http://www.facebook.com/pub/tblake/www/intel.gif HTTP/1.0" 304 -
ppp.a2.ulaval.ca - - [28/Aug/1995:00:00:52 -0400] "GET http://www.datadog.com/pub/job/vk/flowers1.gif HTTP/1.0" 200 4288
shep102.wustl.edu - - [28/Aug/1995:00:02:04 -0400] "GET http://www.facebook.com/pub/pribut/redblsm.gif HTTP/1.0" 200 269
shep102.wustl.edu - - [28/Aug/1995:00:01:27 -0400] "GET http://www.facebook.com/pub/pribut/spsport.html HTTP/1.0" 200 3589
ppp.mia.94.shadow.net - - [28/Aug/1995:00:01:40 -0400] "GET http://www.quora.com/pub/robert/current.html HTTP/1.0" 200 30337
crl12.crl.com - - [28/Aug/1995:00:01:09 -0400] "GET http://www.quora.com/pub/atomicbk/logo2.gif HTTP/1.0" 200 12871 """
        self.alerts = LogAlertsQueue()
        for log in logs.splitlines():
            self.alerts.add(parse_line(log))
            time.sleep(1)

    def test_ignored(self):
        """Test that a missing size is taken as zero """
        self.assertEqual(self.alerts[1].logentry.length, 0)

    def test_above_threshold(self):
        """Test that we print a correct alert with a low threshold.
	We know the avg in this case because we are using static data.
	Criteria for passing the test is that the value is in what's being printed"""
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            process_alerts(self.alerts, duration=2, threshold=100)
            output = out.getvalue().strip()
            self.assertTrue("21604.0" in output)
        finally:
            sys.stdout = saved_stdout

    def test_below_threshold(self):
        """Test that we correctly raise an alert when avg traffic goes below a threshold"""
        self.setUp()
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            process_alerts(self.alerts, duration=2, threshold=100000)
            output = out.getvalue().strip()
            self.assertTrue("below threshold" in output)
        finally:
            sys.stdout = saved_stdout
