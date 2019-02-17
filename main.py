import win32pdh, string, win32api
import pyttsx3
import time
import os

#current file path
this_path = str.replace(os.path.realpath(__file__), __file__, '')

#load our search list
to_search_for = list()

with open(os.path.join(os.path.curdir,'programs.txt')) as f:
    for line in f:
        to_search_for.append(str.replace(line, '\n', ''))

#get current running processes
instances = win32pdh.EnumObjectItems(None,None,'process', win32pdh.PERF_DETAIL_WIZARD)

#ini text-to-speech engine
engine = pyttsx3.init()

#init our states
found_this_time = False
found_last_time = False
found_time = None

#load our previous states
with open(os.path.join(this_path,'save.txt'),'r') as f:
    found_last_time = bool(f.readline() == "True\n")    
    if(found_last_time == True):
       found_time = float(f.readline())

#search for occurances of unproductive processes
for s in to_search_for:
    if(s in instances[1]):
        found_this_time = True
        break

#alert user if process has been open too long
#otherwise save current state
if(found_last_time and found_this_time):
    print(str(time.time() - found_time))
    if(time.time() - found_time > 30):
        print("get back to work")
        engine.say("Get back to work")
        engine.runAndWait()
elif(found_last_time == False and found_this_time == True):
    found_last_time = True
    found_time = time.time()
    with open(os.path.join(this_path,'save.txt'),'w') as f:
        f.write(str(found_last_time)+"\n")
        f.write(str(found_time))
else:
    found_last_time = False
    found_time = None
    with open(os.path.join(this_path,'save.txt'),'w') as f:
        f.write(str(found_last_time)+"\n")
        f.write("None")