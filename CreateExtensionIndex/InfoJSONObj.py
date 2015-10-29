'''
Created on Oct 22, 2015

@author: wujz
'''
# -*- coding: utf-8 -*-  
import re
import json

from common.JSONObj import JSONObj
from common.URILoader import URILoader

class InfoJSONObj:
    KEY_LIST = ['type', 'provider', 'software', 'language', 'category', 'promotion']
    TYPE, PROVIDER, SOFTWARE, LANGUAGE, CATEGORY, PROMOTION = 0,1,2,3,4,5
    RAW_INFO_JSON_URL = 'https://raw.githubusercontent.com/IBMPredictiveAnalytics/repos_name/master/info.json'

    def __init__(self, repo_name):       
        repo_info_json_url = re.sub('repos_name', repo_name, InfoJSONObj.RAW_INFO_JSON_URL)      
        
        try:
            self.repo_info_json = json.loads(URILoader.loadURI(repo_info_json_url, repo_name+"'s info.json file", "Switch to next repo."))
        except ValueError:
            raise Exception("ValueError: "+repo_name+"'s info.json has an illegal format. Please check!"+"Switch to next repo.") 
        except Exception as e:
            raise e    
        
        self.item_list = []
        for key in InfoJSONObj.KEY_LIST:
            try:
                if type(self.repo_info_json[key]) == list:
                    val = self.repo_info_json[key][0]
                else:
                    val = self.repo_info_json[key]
                self.item_list.append(JSONObj(key,val.strip()))
            except:
                raise ValueError("info.json missed some of the items below:\n"
                                 "type, provider, software, language, category, promotion.")  
