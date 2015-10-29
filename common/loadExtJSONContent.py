'''
Created on Oct 27, 2015

@author: wujz
'''
import json
def loadExtJSONContent(ext_path):
    try:     
        fp = open(ext_path,'r',encoding='utf-8')
        ext_content = fp.read()
        fp.close()
        repos_set_json = json.loads(ext_content)
    except ValueError as e:
        raise Exception("ValueError: The {0} has an illegal format. Please check!".format("extension index file"))
    except Exception as e:
        raise e
    return repos_set_json