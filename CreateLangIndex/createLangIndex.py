'''
Created on Oct 27, 2015

@author: wujz
'''
from common.Logger import Logger
from common.loadExtJSONContent import loadExtJSONContent
from common.URILoader import URILoader
from CreateLangIndex.LangPropObj import LangPropObj
import os

LOG_DIR_NAME = 'log'
LANG_DIR = 'lang'
LANG_LIST = ['en', 'de', 'es', 'fr', 'it', 'ja', 'ko', 'pl', 'pt_BR', 'ru', 'zh_CN', 'zh_TW']
EXT_KEY = 'extension_detail_info'
LOG_INFO = 'createLangIndex.log'
RAW_REPO_LANG_URI = 'https://raw.githubusercontent.com/IBMPredictiveAnalytics/{0}/master/src/lang/{1}/{0}_{1}.properties'
RAW_INDEX_KEY = "extension_index"
INDENT = '\t'
LANG_INDEX_PRE = "{\n"+INDENT+"\"extension_lang\":[\n"+INDENT*2

def createLangIndex(*args):
    outdir = args[0]
    ext_path = args[1]
     
    #if product == "modeler":
    #    index_key = RAW_INDEX_KEY.format('modeler')
    #elif product == 'stats':
    #    index_key = RAW_INDEX_KEY.format('stats')
    index_key = RAW_INDEX_KEY
    try:
        try:
            lang_path = os.path.join(outdir,LANG_DIR) 
            os.mkdir(lang_path)
            root_log_dir = os.path.join(outdir, LOG_DIR_NAME)  
            langLogger = Logger(os.path.join(root_log_dir,LOG_INFO),'langLogger')
            langLogger.info("CreateLicenseIndex script start ...")    
            
            langLogger.info("Get extension index  ...")
            repos_set_json = loadExtJSONContent(ext_path)
            repos_set_json_index = repos_set_json[index_key]   
        except Exception as e:  
            raise e
        
        for lang_item in LANG_LIST:
            fp_content = LANG_INDEX_PRE
            langLogger.info("Start to get '"+lang_item+"' file")
            i=0
            for repo in repos_set_json_index:
                try:
                    repo_name = repo["repository"]
                    i+=1
                    langLogger.info(lang_item+": "+str(i)+" repo "+repo_name)
                except Exception:
                    raise Exception("At least one repository in index file does not have repo name. Please check!")    
                
                repo_lang_uri = RAW_REPO_LANG_URI.format(repo_name, lang_item)
 
                try:
                    repo_lang_content = URILoader.loadURI(repo_lang_uri, "language index file")
                    lang_json_str = LangPropObj.convertToJSONStr(repo_name, repo_lang_content)
                except Exception as e:
                    if 'HTTPError' in str(e):
                        # some repositories do not have lang file, by default use en file in index for extension file
                        lang_json_str = LangPropObj.generateJSONStr(repo_name,repo[EXT_KEY]['Summary'],repo[EXT_KEY]['Description'])
                    else:
                        raise e

                fp_content += lang_json_str
                
            try:
                fp_content = fp_content[0:-2]+'\n'+INDENT+']\n}'
                fp = open(os.path.join(lang_path, lang_item+'.json'), 'w', encoding='utf-8') 
                fp.write(fp_content)
                fp.close()
            except Exception as e:
                raise e
                
    except Exception as e:
        langLogger.error(str(e),e)
        langLogger.info("CreatelangIndex action failed!")
        raise e
    finally:
        langLogger.close()
