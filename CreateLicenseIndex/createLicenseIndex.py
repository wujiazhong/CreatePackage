'''
Created on Oct 22, 2015

@author: wujz
'''
# -*- coding: utf-8 -*-  
from common.Logger import Logger
from common.URILoader import URILoader
from common.loadExtJSONContent import loadExtJSONContent
from CreateLicenseIndex.LicenseItemObj import LicenseItemObj
from CreateLicenseIndex.LicenseIndexItemStr import LicenseIndexItemStr
import os

#RAW_REPOS_SET_URI = "https://raw.githubusercontent.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io/master/resbundles/{0}/index_for_{1}.json"
RAW_INDEX_KEY = "extension_index"
RAW_LICENSE_URI = "https://raw.githubusercontent.com/IBMPredictiveAnalytics/{0}/master/LICENSE"
RAW_LICENSE_NAME = "license{0}.txt"
INDENT = '\t'
LICENSE_FILE_NAME = 0
REPOS_NAME_LIST = 1
KEY_LIST = ["license_file_name","repository_names"]
LOG_INFO = "createLicenseIndex.log"
LICENSE_DIR = 'licenses'
LIC_INDEX_FILE = 'extension_license_index.json'
LOG_DIR_NAME = 'log'

def createLicenseIndex(*args):
    outdir = args[0]
    ext_path = args[1]        
    
    #if product.lower() == "modeler":
        #repos_set_uri = RAW_REPOS_SET_URI.format('modeler','modeler')
        #index_key = RAW_INDEX_KEY.format('modeler')
    #elif product.lower() == 'stats':
        # wrong spell of statistics
        #repos_set_uri = RAW_REPOS_SET_URI.format('statisitcs','stats') 
        #index_key = RAW_INDEX_KEY.format('stats')
    index_key = RAW_INDEX_KEY
    try:   
        license_obj_list = []        
        try:
            lic_path = os.path.join(outdir,LICENSE_DIR)   
            os.mkdir(lic_path)
            root_log_dir = os.path.join(outdir, LOG_DIR_NAME) 
            licenseLogger = Logger(os.path.join(root_log_dir,LOG_INFO),'licenseLogger')
            licenseLogger.info("CreateLicenseIndex script start ...")
        except Exception:  
            raise Exception("IOError: Need permission to write in "+outdir)
        
        try:     
            licenseLogger.info("Get extension list  ...")
            repos_set_json = loadExtJSONContent(ext_path)
            repos_set_json_index = repos_set_json[index_key]
        except Exception as e:
            raise e
        
        repo_index = 0
        licenseLogger.info("Start to get license content ...")
        for repo in repos_set_json_index:
            try:
                repo_name = repo["repository"]
            except Exception:
                raise Exception("At least one repository in index file does not have repo name. Please check!")    
            
            repo_license_uri = RAW_LICENSE_URI.format(repo_name)
            
            try:     
                repo_license_content = URILoader.loadURI(repo_license_uri, "license file")
            except Exception as e:
                raise e
    
            isExistedLicense = False
            repo_index += 1
            for item in license_obj_list:
                if repo_license_content == item.getLicenseContent():
                    isExistedLicense = True
                    item.addRepoName(repo_name)
                    break   
            if not isExistedLicense:
                addObj(repo_name, repo_license_content,license_obj_list)
        
        lic_index = 0
        index_content = "{\n"+INDENT+"\"license_index\": [\n";           
        for obj in license_obj_list:
            index_item_str = LicenseIndexItemStr.getItemStr(obj)
            index_content += index_item_str
            lic_index += 1
            licenseLogger.info(str(lic_index)+" license: save in file '"+obj.getLicenseName()+"'.")
            licenseLogger.info("Repos use this license: "+LicenseIndexItemStr.convertListToString(obj.getRepoNameList()))
            
            license_fp = open(os.path.join(lic_path,obj.getLicenseName()),'w',encoding = "utf-8")
            license_fp.write(obj.getLicenseContent())
            license_fp.close()

        index_content = index_content[0:-2]
        index_content += '\n' + INDENT + "]\n}"
        index_fp = open(os.path.join(lic_path,LIC_INDEX_FILE),'w',encoding='utf-8')
        index_fp.write(index_content)
        licenseLogger.info("CreateLicenseIndex action succeeded!")
    except Exception as e:
        licenseLogger.error(str(e),e)
        licenseLogger.info("CreateLicenseIndex action failed!")
        raise e
    finally:
        licenseLogger.info("Totally get "+str(len(license_obj_list))+" type(s) of license from "+str(repo_index)+" repos!")
        licenseLogger.close()
                    
def addObj(repo_name, repo_license_content,license_obj_list):
    license_obj = LicenseItemObj()
    license_obj_list.append(license_obj)
    license_obj.addRepoName(repo_name)
    license_obj.setLicenseContent(repo_license_content)
    license_obj.setLicenseName(RAW_LICENSE_NAME.format(len(license_obj_list)))

        
    
            
        
                    
            
        
        
        
        
        
        
        
        
        
        
        
        