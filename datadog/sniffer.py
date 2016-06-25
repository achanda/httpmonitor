"""Generates a logfile by randomly selecting lines from another given logfile every 2 seconds"""
import sys
import random
import time

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Wrong number of arguments'
    try:
        while True:
            try:
                fr = open(sys.argv[1])
                line = random.choice(fr.readlines())
                fw = open(sys.argv[2], 'a')
            except IOError:
	        print "Could not open file:", sys.argv[2]
                sys.exit(1)
            with fw as myfile:
                myfile.write(line)
            time.sleep(random.randint(0,2))
    except KeyboardInterrupt:
        sys.exit(0)
