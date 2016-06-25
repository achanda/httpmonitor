#!/usr/bin/env python

"""This script runs the main monitor that tails a logfile and processes alerts"""

import sys
from optparse import OptionParser
from collections import Counter

import  parser
import  printer
from alerts import LogAlertsQueue, process_alerts

def main():
    """ Main function for the module"""
    opt_parser = OptionParser(usage="usage: %prog filename")
    opt_parser.add_option("-t", "--threshold", dest="threshold", type="int",
                          help="traffic threshold (in bytes) for alerts")
    opt_parser.add_option("-d", "--duration", dest="duration", type="int",
                          help="interval (in seconds) for alerts")
    (options, args) = opt_parser.parse_args()
    if len(args) != 1:
        opt_parser.error("wrong number of arguments")

    counter = Counter()
    alerts_data = LogAlertsQueue()
    process_alerts(alerts_data, duration=options.duration, threshold=options.threshold)
    for entry in parser.parse(args[0]):
        counter.update([entry.section])
        alerts_data.add(entry)
        printer.print_table(counter)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
