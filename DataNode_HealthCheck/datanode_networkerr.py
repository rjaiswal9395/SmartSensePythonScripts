datanode_log_file = open("temp.txt", 'r') #here temp.txt is the output of Logfilecutter.py
datanode_ip_list = [] #contains the ip of the datanode obtained from the startup message
badlink_ip_list = [] #contains the date, time and also the bad link ip address
def network_error_checker (filename):
    error_count = 0
    a = -1
    for line in filename:
        a = 0
        if "STARTUP_MSG:   host =" in line:
            port = line.split('/')
            if str(port[1]) not in datanode_ip_list:
                datanode_ip_list.append(port[1])
        if "for connect ack  from downstream datanode with firstbadlink" in line:
            error_count = error_count + 1 #number of times the bad link error has occured
            line_split = line.split(' ')
            date_and_time_extraction= line.split(',')
            datetime = date_and_time_extraction[0]
            badlink = str(line_split[21])
            badlink_ip_list.append(datetime + " " + badlink)
    if error_count>0:
        a = 1
    return a
result = network_error_checker(datanode_log_file)
print (result)
