from sys import argv
import re
script, filename, duration = argv
from datetime import timedelta
def recent_date_and_time(filename):
    from datetime import datetime
    for line in reversed(list(open(filename))):
        match = re.search(r'(^\d{4}-\d{2}-\d{2} [0-2][0-3]:[0-5][0-9]:[0-5][0-9])', line)
        if match:
            datetime = datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')
            break
    return datetime
endTime = recent_date_and_time(filename)
startTime = endTime - timedelta(days = int(duration))
def health_check_extractor(filename):
    health_check_lines_list = []
    health_check_file = open("temp.txt", 'w')
    health_check_file.seek(0)
    from datetime import datetime
    for line in reversed(list(open(filename))):
        match = re.search(r'(^\d{4}-\d{2}-\d{2} [0-2][0-3]:[0-5][0-9]:[0-5][0-9])', line)
        if match:
            currentTime = datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')
            if  currentTime <= startTime :
                break
        health_check_lines_list.append(line)
    for line in reversed(health_check_lines_list):
        health_check_file.write(line)
health_check_extractor(filename)









