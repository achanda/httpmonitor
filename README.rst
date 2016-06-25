## Running the log generator
python datadog/sniffer.py ./assets/dump2.log </path/to/logfile>

## Running the monitor
python datadog/monitor.py </path/to/logfile> --threshold 2 --duration 5

## Running tests
python run_tests.py

## Known issues
The parser cannot handle dashes in host names

## Improvements
* The bug that host name can not have dashes should be fixed
* Scheduling the `process_alerts` function using `Timer` is a hack. This should be done using only one thread and suspending it as needed.
* Threads should not be daemonized, this was done so that all threads exit when the main thread is interrupted. But this prevents proper cleanup.
* The whole project should be better organized using a cookie cutter template
* setup.py should be better setup, integrated with tox
* The project should support py33 (currently py26 and py27)
* This will not scale properly with size of logfile since it keeps the counter in main memory. Ideally, this should be distributed across a number of machines and later collected while reporting. In such an architecture, consistency can be acheived by using [CRDTs] (https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)
* Using a language that allows handling memory at a lower level might yield some benefits (Rust, Go)
* Tests for the alerts module is a hack, the module should be re-written to be testable
* It might have been better to generate log files randomly. But I chose to randomly select form a given log file so that entries look real world, at least.
* Alerts should be written to a file, right now an user can scroll up and see old alerts. But that is sloppy.
* The UI is rudimentary, it uses Ctrl+L to clear the screen. This should be done using ncurses.
