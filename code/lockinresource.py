#!/usr/bin/env python

#-----------------------------------------------------------------------
# lockinresource.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from threading import Thread, RLock

#-----------------------------------------------------------------------

class BankAcct:
    
    def __init__(self):
        self._balance = 0
        self._lock = RLock()
        
    def getBalance(self):
        self._lock.acquire()
        try:
            return self._balance
        finally:
            self._lock.release()
            
    def deposit(self, amount):
        self._lock.acquire()
        temp = self._balance
        temp += amount
        print(temp)
        self._balance = temp
        self._lock.release()
        
    def withdraw(self, amount):
        self._lock.acquire()
        temp = self._balance
        temp -= amount
        print(temp)
        self._balance = temp
        self._lock.release()

#-----------------------------------------------------------------------

class DepositThread (Thread):
    
    def __init__(self, bankAcct):
        Thread.__init__(self)
        self._bankAcct = bankAcct
        
    def run(self):
        for i in range(10):
            self._bankAcct.deposit(1)

#-----------------------------------------------------------------------

class WithdrawThread (Thread):
    
    def __init__(self, bankAcct):
        Thread.__init__(self)
        self._bankAcct = bankAcct
        
    def run(self):
        for i in range(5):
            self._bankAcct.withdraw(2)

#-----------------------------------------------------------------------

def main():
    
    bankAcct = BankAcct()
    
    depositThread = DepositThread(bankAcct)
    withdrawThread = WithdrawThread(bankAcct)
    
    depositThread.start()
    withdrawThread.start()
    
    depositThread.join()
    withdrawThread.join()
    
    print('Final balance:', bankAcct.getBalance())

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
