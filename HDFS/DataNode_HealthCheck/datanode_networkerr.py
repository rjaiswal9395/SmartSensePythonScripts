"""
    Python program to check for any network errors in a given file.
    In the command line enter something like this:
    python  neterrfi.py  /input_file_location  /location_where_you_want_the_result_to_be_written
"""
import os
import sys
import re

script, input_file_path, output_file_path = sys.argv


def networkErrorChecker(input_filepath, output_path):
    """
    Funtion name:networkErrorChecker
    Checks whether there are any network errors in a given file. And writes the result into a file in the same output
    path location with the name "network_error_result.txt"
    It writes -1 into the result file if: it is unable to open the file in the given mentioned input file location or
                                          if no such file exists.
    It writes 0 into the result file if: no network errors are found in the given input file.
    It writes 1 into the result file if: It has found any network errors in the given file.
    :param input_filepath: taken from the command line arguments.
    :param output_path:  taken from the command line arguments.
    :return: returns the error list

    """
    error_check_result = -1
    datetime_datanode_errorIp_list= []
    error_count =0
    if os.path.exists(input_file_path):
        with open(input_filepath,'r') as file_to_be_read:
            error_check_result = 0
            datanode = ""
            for line in file_to_be_read:
                datanode_ip = re.findall('host =.*\/(.*)', line)
                if datanode_ip:
                    datanode = datanode_ip
                error_ip = re.findall('for connect ack  from downstream datanode with firstbadlink as (.*)', line)
                if error_ip:
                    error_count = error_count + 1
                    datetime = re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                    if datetime and datanode:
                        datetime_datanode_errorIp_list.append(str(datetime)+" " +str(datanode) +" " + str(error_ip))
            if error_count > 0:
                error_check_result = 1
    with open(output_path + "/network_error_result.txt",'w') as output_file:
        output_file.write(str(error_check_result))
    return datetime_datanode_errorIp_list

def main():
    networkErrorChecker(input_file_path, output_file_path)

main()