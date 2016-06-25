"""Parses a file to return formatted log entries"""

import re

from models import LogEntry
from tail import follow

# TODO handle dashes in names
REGEX = r'([\d\.|\w\.]+)\s(\S*)\s(\S*)\s\[(.*?)\]\s"(.*?)"\s(\d+)\s(\S*)'

def parse_line(line):
    """Parses one line and returns a LogEntry object if successful"""
    pattern = re.compile(REGEX)
    result = pattern.match(line, re.I)
    if result != None:
        part = result.groups()
        return LogEntry(part[0], part[3], part[4], part[5], part[6])
    return None

def parse(filename):
    """Parses the given file line by line
    while following it"""
    try:
        fd = open(filename)
    except IOError:
        print "Could not read file:", filename
    lines = follow(fd)
    for line in lines:
        parsed = parse_line(line)
        if parsed == None:
            continue
        yield parsed
