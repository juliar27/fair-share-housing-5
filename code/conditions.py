#!/usr/bin/env python

#-----------------------------------------------------------------------
# conditions.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from threading import Thread, RLock, Condition

#-----------------------------------------------------------------------

class BankAcct:
    
    def __init__(self):
        self._balance = 0
        self._lock = RLock()
        self._condition = Condition(self._lock)
        
    def getBalance(self):
        self._lock.acquire()
        try:
            return self._balance
        finally:
            self._lock.release()
            
    def deposit(self, amount):
        self._condition.acquire()
        self._balance += amount
        print(self._balance)
        self._condition.notifyAll()
        self._condition.release()
        
    def withdraw(self, amount):
        self._condition.acquire()
        while self._balance < amount:
            self._condition.wait()
        self._balance -= amount
        print(self._balance)
        self._condition.release()

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
