"""
   A python script to find out the information about the log file provided
   and to also extract the data from the log file in a particular time period

   In the command line please enter the something like this:
   "python  lfcfinal.py  /inputlogfilepath  /outputwrtiepath  int(number of days you want the data to be grepped)"
"""
import os
import re
import sys
from datetime import timedelta
from datetime import datetime

script, read_path, write_path,number_of_days = sys.argv


def logFilePathChecker(path):
    """
    Function name:logFilePathChecker
    A simple function to check whether the input file exists or not
    :param path: The read path entered in the command line arguments
    :return:Returns 1 if the path exists
    """
    if not os.path.exists(path):
        print("The log file doesn't exist")
        sys.exit(0)
    return 1

def logFileDetector(file):
    """
    Function name: logFileDetector
    Checks which logfile it is
    :param file: Path of the input file(read_path)
    :return: returns the match, if its a datanode file, it returns datanode.DataNode
    """
    with open(file, 'r') as file_to_be_checked:
        for line in file_to_be_checked:
            logmatch = re.search(r'datanode.DataNode|namenode.NameNode|metastore.HiveMetaStore|server.HiveServer2', line)
            if logmatch:
                file_detect_result = logmatch.group() + ".txt"
                break
    return file_detect_result

def logFileEndTimeDetector(file):
    """
    Funtion name: logFileEndTimeDetector
    Finds out whats the last time entry. That is the most recent time in the log file
    :param file: Path of the input file  (read_path)
    :return: returns the most recent time entry, i.e. the end time of the log file
    """
    with open(file, 'r') as file_to_check:
        for line in reversed(list(file_to_check)):
            match = re.search(r'(^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if match:
                end_time = datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')
                break
    return end_time

def startTimeFinder(end_time,day_count):
    """
    Function name: startTimeFinder
    It finds the start time starting from which the log file should be extracted
    :param end_time: return value of the logFileEndTimeDetector
    :param day_count: It is taken from the command line argument
    :return: returns the start time
    """
    start_time = end_time - timedelta(days = int(day_count))
    return start_time

def logFileLineExtractor(filename, startTime):
    """
    Function name: logFileLineExtractor
    Extracts lines from the log file in the required time range. Checks for the file in reverse and stops extracting
    when the startTime is found.
    :param filename: Path of the input file (read_path)
    :param startTime: return value of the startTimeFinder
    :return: all the required lines are appended to a list and the list is returned.
    """
    health_check_lines_list = []
    with open(filename, 'r') as file_to_be_extracted:
        for line in reversed(list(file_to_be_extracted)):
            match = re.search(r'(^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if match:
                currentTime = datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')
                if currentTime <= startTime:
                    break
            health_check_lines_list.append(line)
    return health_check_lines_list

def cutLogFileWriter(writepath,filename,list):
    """
    Funtion name: cutLogFileExtractor
    It creates a file, with the name as "filename" in the write path location and writes from the list which is
    opened in reverse.
    :param writepath: taken from the command line arguements, the path where we want the extracted log file to be
                      written.
    :param filename: The name of the file, i.e the return value of the logFileDetector
    :param list: return value of the function logFileLineExtractor
    :return: returns 1 after writing the lines into the file, indicating that the operation is finished.
    """
    with open(writepath + "/" + filename, 'w') as health_check_file:
        health_check_file.seek(0)
        for line in reversed(list):
            health_check_file.write(line)
    return 1

def main():
    """
    It calls all the funtions in order, for the extraction process
    :return: returns 1 indicating that the process is finished.
    """
    logFilePathChecker(read_path)
    file_name = logFileDetector(read_path)
    endTime = logFileEndTimeDetector(read_path)
    startTime = startTimeFinder(endTime, number_of_days)
    health_check_list = logFileLineExtractor(read_path, startTime)
    cutLogFileWriter(write_path, file_name, health_check_list)
    return 1


main()