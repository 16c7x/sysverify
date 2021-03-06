#!/usr/bin/env python

from optparse import OptionParser
import yaml
import os, sys
import logging
import subprocess

yamlDir = '/etc/sysverify.d/'
os.system('clear')
testRC    = 0
totalTest = 0

class rcolors:
    RESET   = '\033[0m'
    BLACK   = '\033[90m'
    GREEN   = '\033[92m'
    RED     = '\033[91m'
    BLUE    = '\033[94m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    YELLOW  = '\033[93m'
    MAGENTA = '\033[95m'
    DEFAULT = '\033[99m'

def getCmdLine():
    """Sets up OptParse to fetch cmd line options and
    returns the (options, args) tuple"""
    usage = "SysVerify.py -f <filename> -l <logfile>"
    parser = OptionParser(usage)
    parser.add_option("-f", "--filename", help="YAML file containing test specification")
    parser.add_option("-l", "--logfile", help="The log file to send your results to")

    return parser.parse_args()

def setupLogging(loglevel="SysVerify", filename="sysverify.log"):
    """Sets up logging file and returns the logging handler
    :param loglevel: Log Level Name. defaults to 'SysVerify'
    :type string:
    :param filename: Where to output the log file. Defaults to 'sysverify.log'
    :type string:
    :returns: logging handler which you can use like logger.info("<my message>")
    """
    logger = logging.getLogger(loglevel)
    hdlr = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    return logger

class Test:
    """Test Object"""
    output = ""
    test = ""
    comment = ""
    command = ""

    def __init__(self, test_data):
        """Test Constructor
        :param test_data: Dictionary containing the test name, comment & command to run
        :type dictionary:"""
        try:
            self.test = test_data.get('test')
        except KeyError:
            print "Invalid test formatting, must have a 'test' key in the input file"
            print test_data

        try:
            self.comment = test_data.get('comment')
        except KeyError:
            print "Invalid test formatting, must have a 'comment' key in the input file"
            print test_data

        try:
            self.command = test_data.get('command')
        except KeyError:
            print "Invalid test formatting, must have a 'command' key in the input file"
            print test_data

    def __str__(self):
         return "%s:`%s`" %(self.test, self.comment)

    def runCommand(self):
        """ Executes the test command and returns the output string.  Normally a 'PASS' or 'FAIL' string"""
        try:
            outPut = subprocess.Popen(self.command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            status =  outPut.communicate()[0]

            return status.rstrip('\n')
        except:
            print "FAILURE when trying to execute command: %s" % (self.command,)
            print "In Test", self
            sys.exit(1)

def parseTests(fileName, testName):
    """Reads YAML source file and parses it into an array of Test classes. Returns the array
    :param filename: Yaml formatted file to read. Defaults to './SysTest.yaml'
    :type string:
    """
    stream1 = open(fileName, 'r')
    dataMap = yaml.load(stream1)
    stream1.close()
    print ' '
    print rcolors.YELLOW +'Running test for ' +testName +rcolors.RESET
    testList = [ Test(dataMap[x]) for x in dataMap ]

    return testList

def runTests(testList):
    """Runs a series of tests and outputs an array of the result messages
    :param testList: array of tests
    :type class Test:
    """

    return [ "%s\t=> %s"%(str(x), x.runCommand()) for x in testList ]

def printResults(testResults):
    """Formats and outputs test results.  If log handle present will write results to log file
    :param testResults: array of strings representing the results to print out
    :type [str,]:
    :param logger: log handle to handle syslog messages
    """
    index = 0
    global testRC
    while index < len(testResults):
        testResults[index] = testResults[index].rstrip('\n')
        checkFail = testResults[index]
        if 'fail' in checkFail.lower():
            testRC += 1
        index += 1
    for test in testResults:
        print moduleName+': '+test
        if logger:
            logger.info(moduleName+': '+test)

def doIt(doFile, doName):
    global totalTest
    testList = parseTests(doFile, doName)
    lenList = str(len(testList))
    totalTest = totalTest + int(lenList)
    print rcolors.CYAN +"# of tests =>" +lenList +rcolors.RESET
    print "Running Tests"
    results = runTests(testList)
    print "\nResults\n"
    printResults(results)

if __name__ == '__main__':
    print "Gathering cmd line options"
    (options, args) = getCmdLine()
    print "Setting up Logging"
    if options.logfile is None:
        options.logfile = '/var/log/sysverify.log'
    logger = setupLogging('SysVerify', options.logfile)
    print "parsing YAML files"
    if options.filename is None:
        newFileS = os.listdir(yamlDir)
        for FILE in newFileS:
            moduleName = FILE.split('.')[0]
            sourceFile = yamlDir+FILE
            doIt(sourceFile, moduleName)
    else:
        inFile = os.path.isfile(options.filename)
        if inFile:
            moduleName = os.path.basename(options.filename)
            moduleName = moduleName.split('.')[0]
            doIt(options.filename, moduleName)
        else:
            print ' '
            print 'File %s %s %s does not exist' % (rcolors.RED, options.filename, rcolors.RESET)

    print ' '
    print "Finished with", str(testRC), "failed test out of", totalTest
    sys.exit(testRC)
