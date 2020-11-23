#!/usr/bin/env python

#-----------------------------------------------------------------------
# deadlock.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from threading import Thread, RLock

#-----------------------------------------------------------------------

class BankAcct:
    
    def __init__(self, title):
        self._title = title
        self._balance = 0
        self._lock = RLock()
   
    def transferTo(self, other, amount):
        self._lock.acquire()
        other._lock.acquire()
        self._balance -= amount
        other._balance += amount
        print(self._title + ': ' + str(self._balance))
        print(other._title + ': ' + str(other._balance))
        other._lock.release()
        self._lock.release()

#-----------------------------------------------------------------------

class AliceToBobThread (Thread):
    
    def __init__(self, aliceAcct, bobAcct):
        Thread.__init__(self)
        self._aliceAcct = aliceAcct
        self._bobAcct = bobAcct
        
    def run(self):
        for i in range(1000):
            self._aliceAcct.transferTo(self._bobAcct, 1)
            
#-----------------------------------------------------------------------

class BobToAliceThread (Thread):
    
    def __init__(self, bobAcct, aliceAcct):
        Thread.__init__(self)
        self._bobAcct = bobAcct
        self._aliceAcct = aliceAcct
        
    def run(self):
        for i in range(1000):
            self._bobAcct.transferTo(self._aliceAcct, 1)
 
#-----------------------------------------------------------------------

def main():
    
    aliceAcct = BankAcct('Alice')
    bobAcct = BankAcct('Bob')

    aliceToBobThread = AliceToBobThread(aliceAcct, bobAcct)
    bobToAliceThread = BobToAliceThread(bobAcct, aliceAcct)

    aliceToBobThread.start()
    bobToAliceThread.start()

    aliceToBobThread.join()
    bobToAliceThread.join()

    print('Finished')

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
