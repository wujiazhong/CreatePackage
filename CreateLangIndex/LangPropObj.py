'''
Created on Oct 27, 2015

@author: wujz
'''
from common.JSONObj import JSONObj
from configparser import ConfigParser
INDENT = '\t'
LANG_JSON_KET = ['Name', 'Summary', 'Description']

class LangPropObj:
    @staticmethod
    def convertToJSONStr(repo_name, propStr):
        config = ConfigParser()
        con = '[tag]\n'+propStr
        config.read_string(con)
        
        for item in config.sections():
            jsonStr = INDENT*2+'{\n'+INDENT*3+JSONObj.createJSONStr('name',repo_name)
            for key in config.options(item):
                jsonStr += INDENT*3+JSONObj.createJSONStr(key, config.get(item, key))
        
        return jsonStr[0:-2]+'\n'+INDENT*2+'},\n'
    
    @staticmethod
    def generateJSONStr(name, summary, descr):
        json_str = INDENT*2+'{\n'
        json_str += INDENT*3 + JSONObj.createJSONStr(LANG_JSON_KET[0], name)
        json_str += INDENT*3 + JSONObj.createJSONStr(LANG_JSON_KET[1], summary)
        json_str += INDENT*3 + JSONObj.createJSONStr(LANG_JSON_KET[2], descr)
        return json_str[0:-2]+'\n'+INDENT*2+'},\n'
        