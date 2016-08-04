import csv
import re
import datetime
import subprocess
from datetime import *
from datetime import timedelta

def reader(filepath):
    print(filepath+" opened for processing\n")
    return open(filepath,"r")

def keyword_extractor(text_found,filevariable):
  filevariable.seek(0);
  Startup_Messages=[]
  Errors=[]
  Dir=[]
  count=0
  for line in reversed(list(filevariable)):
    str_list = ("".join(line))
    if text_found in str_list:
      Errors.append(str_list)
      Dir.append((str_list.split("/",1)[1]).split(" ",1)[0])
      count=count+1

  print( "Total ", count, " Instances Found\n")
  return Startup_Messages,Errors,count,Dir

def parser(file):
    startup_msg,errors,count,dir=keyword_extractor("Invalid dfs.datanode.data.dir",file)


def main():
    path="../Log_Files_For_Parsing/hadoop-hdfs-datanode-hbs1.hwxblr.com.log"
    opened_file=reader(path)
    parser(opened_file)
main()

##