## HTTP log monitoring console program ##

Create a simple console program that monitors HTTP traffic on your machine:

* Consume an actively written-to w3c-formatted HTTP access log (https://en.wikipedia.org/wiki/Common_Log_Format)
* Every 10s, display in the console the sections of the web site with the most hits (a section is defined as being what's before the second '/' in a URL. i.e. the section for "http://my.site.com/pages/create' is "http://my.site.com/pages"), as well as interesting summary statistics on the traffic as a whole.
* Make sure a user can keep the console app running and monitor traffic on their machine
* Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = {value}, triggered at {time}”
* Whenever the total traffic drops again below that value on average for the past 2 minutes, add another message detailing when the alert recovered
* Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons.
* Write a test for the alerting logic
* Explain how you’d improve on this application design

## Running the log generator ##
python datadog/sniffer.py ./assets/dump2.log </path/to/logfile>

## Running the monitor ##
python datadog/monitor.py </path/to/logfile> --threshold 2 --duration 5

## Running tests ##
python run_tests.py

## Known issues ##
The parser cannot handle dashes in host names

## Improvements ##
1. The bug that host name can not have dashes should be fixed
2. Scheduling the `process_alerts` function using `Timer` is a hack. This should be done using only one thread and suspending it as needed.
3. Threads should not be daemonized, this was done so that all threads exit when the main thread is interrupted. But this prevents proper cleanup.
4. The whole project should be better organized using a cookie cutter template
5. setup.py should be better setup, integrated with tox
6. The project should support py33 (currently py26 and py27)
7. This will not scale properly with size of logfile since it keeps the counter in main memory. Ideally, this should be distributed across a number of machines and later collected while reporting. In such an architecture, consistency can be acheived by using [CRDTs] (https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)
8. Using a language that allows handling memory at a lower level might yield some benefits (Rust, Go)
9. Tests for the alerts module is a hack, the module should be re-written to be testable
10. It might have been better to generate log files randomly. But I chose to randomly select form a given log file so that entries look real world, at least.
* Alerts should be written to a file, right now an user can scroll up and see old alerts. But that is sloppy.
* The UI is rudimentary, it uses Ctrl+L to clear the screen. This should be done using ncurses.
