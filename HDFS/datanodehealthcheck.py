import sys
import os
import csv

cwd = os.getcwd()
new=os.path.abspath('..')
sys.path.insert(0, new)

import HDFS.DataNode_HealthCheck.datanode_permission as invaliddatanode
script,input_file_path, write_path= sys.argv
flag=-1

def checkmaster(input_file_path, write_path,string,solution):

  flag= invaliddatanode.maincheck(input_file_path, write_path,string)

  if (flag >=1):
    print("{0} error occured".format(string))
    print(solution)
    print("Error Logs Written to {0}".format(write_path))
  elif (flag == 0):
    print("No {0} error found".format(string))
  elif (flag == -1):
    print("The above error occured during log file parsing")
  print("--------------------------------")


if __name__ == '__main__':
  w=open(write_path,"w")
  w.close()
  with open("Error_Sheet.csv", "rb") as f:
    reader = csv.reader(f, delimiter=",")
    for i,line in enumerate(reader):
        print(" ")
        print("----------------------------------")
        print("Performing {0} Check for {1} error".format(line[0],line[1]))
        checkmaster(input_file_path, write_path,str(line[1]),str(line[2]))



