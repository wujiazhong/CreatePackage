'''
Created on Oct 22, 2015

@author: wujz
'''
import urllib.request
import socket

class URILoader:
    HTTP_ERROR_MSG = "HTTPError: Cannot get connection to Github.com or {0} does not exist. Please check! "
    UNIDEC_ERROR_MSG = "UnicodeDecodeError: The {0} contains non-unicode characters. Please check! "
    UNKNOWN_ERROR_MSG = "Exception: The {0} has an unknown error. Please check! "
       
    @staticmethod
    def loadURI(uri, file_name, sur_msg=''):   
        socket.setdefaulttimeout(600)     
        try:    
            repos_set_json = urllib.request.urlopen(uri, None, 600).read().decode('utf-8')        
        except urllib.error.HTTPError:
            raise Exception(URILoader.HTTP_ERROR_MSG.format(file_name)+sur_msg)           
        except UnicodeDecodeError:
            raise Exception(URILoader.UNIDEC_ERROR_MSG.format(file_name)+sur_msg)
        except Exception:
            raise Exception(URILoader.UNKNOWN_ERROR_MSG.format(file_name)+sur_msg)      
        return repos_set_json
        