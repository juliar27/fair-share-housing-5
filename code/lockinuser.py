#!/usr/bin/env python

#-----------------------------------------------------------------------
# lockinuser.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from threading import Thread, RLock

#-----------------------------------------------------------------------

class BankAcct:
    
    def __init__(self):
        self._balance = 0
        self._lock = RLock()
        
    def acquireLock(self):
        self._lock.acquire()
        
    def releaseLock(self):
        self._lock.release() 
        
    def getBalance(self):
        return self._balance
        
    def deposit(self, amount):
        temp = self._balance
        temp += amount
        print(temp)
        self._balance = temp
        
    def withdraw(self, amount):
        temp = self._balance
        temp -= amount
        print(temp)
        self._balance = temp
        
#-----------------------------------------------------------------------

class DepositThread (Thread):
    
    def __init__(self, bankAcct):
        Thread.__init__(self)
        self._bankAcct = bankAcct
        
    def run(self):
        for i in range(10):
            self._bankAcct.acquireLock()
            self._bankAcct.deposit(1)
            self._bankAcct.releaseLock()
            
#-----------------------------------------------------------------------

class WithdrawThread (Thread):
    
    def __init__(self, bankAcct):
        Thread.__init__(self)
        self._bankAcct = bankAcct
        
    def run(self):
        for i in range(5):
            self._bankAcct.acquireLock()
            self._bankAcct.withdraw(2)
            self._bankAcct.releaseLock()
            
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
