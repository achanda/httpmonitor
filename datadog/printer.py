"""Prints a given dict on the screen"""
import sys

def print_table(data):
    """Clears the screen and prints the given dict"""
    sys.stderr.write("\x1b[2J\x1b[H")
    print "{:<50} {:<10}".format('Segment', 'Count')
    for k, v in data.iteritems():
        print "{:<50} {:<10}".format(k, v)
    segments = data.most_common(3)
    print "\n\nTop three segments with most hits are:"
    for segment in segments:
        print segment[0]
