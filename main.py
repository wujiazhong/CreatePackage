'''
Created on Oct 22, 2015

@author: wujz
'''
from optparse import OptionParser 
from common.Logger import Logger
from common.runScriptThread import runScriptThread
from CreateLicenseIndex.createLicenseIndex import createLicenseIndex
from CreateExtensionIndex.createExtensionIndex import createExtensionIndex 
from CreateLangIndex.createLangIndex import createLangIndex 
from common.packageTool import zip_dir
import os,traceback,shutil
LOG_DIR_NAME = 'log'
PACAKAGE_NAME = "Package"
LOG_NAME = 'main.log'
ABBR_PRODUCT = 'stats'
WHOLE_PRO_NAME = 'Statistics'
ZIP_NAME = 'extension_index_resbundles'    
 
if __name__ == '__main__':
    usage = "usage: %prog [options] arg1"  
    parser = OptionParser(usage)  
    parser.add_option("-o", "--outdir", dest="outdir", action='store', help="Directory to save Statistics.zip")
    #parser.add_option("-p", "--product", dest="productName", action='store', help="Choose license index for which product: 1. modeler 2. stats.")
    (options, args) = parser.parse_args() 
    
    if not os.path.isdir(options.outdir):
        parser.error("Please input a valid directory to save Statistics.zip.")
    #if options.productName.lower() != "modeler" and options.productName.lower() != "stats":  
    #    parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
    
    try: 
        savePath = os.path.join(options.outdir,PACAKAGE_NAME)
        if os.path.isdir(savePath):
            print("The output folder "+savePath+" already existed. Delete it to create a new one or exit?(y/n):")
            ch = input()
            
            if ch.lower() != 'y':
                print("Please choose another folder.")
                exit(-1)
            else:
                try:
                    os.system(r"C:\Windows\System32\attrib -r "+ savePath+"\*.* " + " /s /d")
                    shutil.rmtree(savePath, ignore_errors = True)
                except:
                    raise Exception("Cannot get administrator permission to delete "+savePath)
        #savePath = os.path.join(r'C:\Users\wujz\Desktop',PACAKAGE)
        logPath = os.path.join(savePath,LOG_DIR_NAME)
        os.mkdir(savePath)
        os.mkdir(logPath)
        
        mainLogger = Logger(os.path.join(logPath,LOG_NAME),'mainLogger')
        
        try:
            mainLogger.info("Main Script start ... ")
            
            # create index for extension
            mainLogger.info("'CreateExtensionIndex start...")
            ext_path = createExtensionIndex(savePath, ABBR_PRODUCT) 
            mainLogger.info("'CreateExtensionIndex complete...")
            
            '''
            Description: create two threads -- one aimed at creating license index; the other aimed at creating lang index
            '''
            # create thread to get index for license
            mainLogger.info("'CreateLicenseIndex thread start...")
            runCreateLicenseIndex = runScriptThread(createLicenseIndex, savePath, ext_path)
            runCreateLicenseIndex.setDaemon(True)
            runCreateLicenseIndex.start()

            # create thread to get index for language
            mainLogger.info("CreateLangIndex thread start ...")
            runCreateLangIndex = runScriptThread(createLangIndex, savePath, ext_path)
            runCreateLangIndex.setDaemon(True)
            runCreateLangIndex.start()
            
            runCreateLicenseIndex.join()
            runCreateLangIndex.join()
            
            if runCreateLicenseIndex.exitcode!=0:
                raise Exception('Exception in ' + runCreateLicenseIndex.getName()+'\n'+runCreateLicenseIndex.exc_traceback)
            
            if runCreateLangIndex.exitcode!=0:
                raise Exception('Exception in ' + runCreateLangIndex.getName()+'\n'+runCreateLangIndex.exc_traceback)
            
            mainLogger.info("'CreateLicenseIndex' thread complete...")
            mainLogger.info("'CreateLangIndex' thread complete...")
            
            # start to compress files to ZIP
            if not runCreateLangIndex.isAlive() and not runCreateLicenseIndex.isAlive():
                mainLogger.info("Start to compress files into package ...")
                zippath = os.path.join(savePath,ZIP_NAME+'.zip')
                zip_dir(savePath, zippath)
                mainLogger.info("Compression complete ...")
            
        except Exception as e:
            mainLogger.error(str(e),e)
            raise e  
        finally:
            mainLogger.close()      
    except Exception as e:
        print(str(traceback.format_exc()))
    except IOError:
        print(str(traceback.format_exc()))
        print("Need permission to create folder in "+options.outdir+" or the destination already contains a folder named '"+PACAKAGE_NAME+"'")        
