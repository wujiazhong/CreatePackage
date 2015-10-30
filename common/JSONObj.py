'''
Created on Oct 22, 2015

@author: wujz
'''
import re

class JSONObj:
    # escape " to \"
    def __init__(self, key, val):
        self.key, self.val = escapeStr(key), escapeStr(val)
    
    def getJSONStr(self):
        return "\""+self.key+"\":\""+ self.val +"\",\n"
    
    @staticmethod
    def createJSONStr(key, value):
        return "\""+escapeStr(key)+"\":\""+ escapeStr(value) +"\",\n"
    

def escapeStr(raw_str):  
    map_list = [ 
                    (re.compile(r'\\(?!u[0-9a-fA-F]{4})'), r'\u005C'),  # '\' is illegal char in json
                    (re.compile(r'\"'), r'\u0022')      # '"' is illegal char in json
                ]  
    
    for item in map_list:
        raw_str = re.sub(item[0],item[1],raw_str)
        
    return raw_str
        
        