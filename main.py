#! /usr/bin/python

import time
import sys

#print(sys.argv[1])

if '-start' in sys.argv:
    file = open('time.txt','w')
    file.write(str(time.time()))
    file.close()
elif '-save' in sys.argv:
    file = open('time.txt','r')
    time_read = float(file.readline())
    file.close()
    file = open('saved_times.txt','a')
    diff_time = time.time() - time_read
    file.write("".join([time.ctime(),' ',str(int(diff_time/3600)),'hours,',str(int((diff_time%3600)/60)),'mins,',str(int((diff_time%3600)%60)),'seconds','\n']))
    file.close()
else:
    #elif '-stop' in sys.argv:
    file = open('time.txt','r')
    time_read = float(file.readline())
    diff_time = time.time() - time_read
    #print(int(diff_time), 'seconds')
    print(int(diff_time/3600),'hours,',int((diff_time%3600)/60),'mins,',int((diff_time%3600)%60),'seconds')
    
