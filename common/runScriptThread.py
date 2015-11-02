'''
Created on Oct 27, 2015

@author: wujz
'''
import threading

class runScriptThread(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, funcName, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.funcName = funcName
    
    def run(self): #Overwrite run() method, put what you want the thread do here
        try:
            self.funcName(*(self.args)) 
        except Exception as e:
            raise e           