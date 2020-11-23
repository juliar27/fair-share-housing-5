#!/usr/bin/env python

#-----------------------------------------------------------------------
# sharing.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from threading import Thread

globalVar = 0

#-----------------------------------------------------------------------

class MyThread (Thread):
    
    def run(self):
        global globalVar
        globalVar = 1
        print('child thread terminated with globalVar =', globalVar)

#-----------------------------------------------------------------------

def main():
    
    global globalVar
    
    myThread = MyThread()
    myThread.start()
    myThread.join()
    
    print('parent thread terminated with globalVar =', globalVar)    

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
