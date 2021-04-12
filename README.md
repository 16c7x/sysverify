Gitlab project path..
http://gitlab.cummins.com/cbs_rpm/Sysverify

There are several ways to run sysverify.

1. It can be run with user defined options via the command lie ```/usr/local/script/sysverify -f /tmp/test.yaml -l /tmp/log``` .This is useful if your debugguing something and want to run one test over an over again.

2. It can be run using its default options by simply running ```/usr/local/script/sysverify```. This will output logs to logfile /var/log/sysverify.log and will use all yaml files in /etc/sysverify.d/

Sysverify outputs the test results to the screen and to a user defined or default logfile, it also gives a count of failed tests in its exit status, this is useful for automating testing. 


Example:
--------
```
Gathering cmd line options
Setting up Logging
parsing YAML files

Running test for test
# of tests =>2
Running Tests

Results

test: Test1:`Check if puppet is running as a service`   => Fail
test: Test2:`Check if opsunix is able to access the machine`    => Pass

Finished with 1 failed test out of 2
[root@ftdcsllrpmbld02 script]# echo $?
1
```