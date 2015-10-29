'''
Created on Oct 22, 2015

@author: wujz
'''
# -*- coding: utf-8 -*-  
import logging,traceback

# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
class Logger:
    def __init__(self, filename, loggerName):
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")  
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)   
        self.filename = filename 
        
        try:       
            self.addFileHandler(filename, formatter)
            self.addStreamHandler(formatter)
        except Exception as e:
            raise e
           
    def debug(self, msg):
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.info(msg)
    def warning(self, msg):
        self.logger.warning(msg)
    def error(self, msg, e):
        if isinstance(e, Exception):
            einfo = str(traceback.format_exc())
            msg += '\n'+ einfo        
        self.logger.error(msg)
    def addFileHandler(self, filename, formatter):
        self.fh = logging.FileHandler(filename)
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(formatter)
        self.logger.addHandler(self.fh)
    
    def addStreamHandler(self, formatter):
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(formatter)      
        self.logger.addHandler(self.ch)
        
    def close(self):
        self.logger.removeHandler(self.fh)
        self.logger.removeHandler(self.ch)
        self.fh.close()
        self.ch.close()
        