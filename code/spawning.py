#!/usr/bin/env python

#-----------------------------------------------------------------------
# spawning.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from threading import Thread

#-----------------------------------------------------------------------

class PrinterThread (Thread):
    
    def __init__(self, color):
        Thread.__init__(self)
        self._color = color
        
    def run(self):
        for i in range(10):
            print(self._color)
        print(self._color + ' thread terminated')

#-----------------------------------------------------------------------

def main():
    
    blueThread = PrinterThread("blue")
    redThread = PrinterThread("red")
    
    blueThread.start()
    redThread.start()
    
    print('main thread terminated')

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
