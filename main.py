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

import os,traceback,zipfile

LOG_DIR_NAME = 'log'
PACAKAGE = "Package"
LOG_NAME = 'main.log'
ZIP_NAME = '{0}.zip'
 
if __name__ == '__main__':
    '''
    usage = "usage: %prog [options] arg1"  
    parser = OptionParser(usage)  
    parser.add_option("-s", "--savedir", dest="savedir", action='store', help="Directory to save Statistics.zip")
    parser.add_option("-p", "--product", dest="productName", action='store', help="Choose license index for which product: 1. modeler 2. stats.")
    (options, args) = parser.parse_args() 
    
    if not os.path.isdir(options.savedir):
        parser.error("Please input a valid directory to save Statistics.zip.")
    if options.productName != "modeler" and options.productName != "stats":  
        parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")'''
    
    try: 
        #savePath = os.path.join(options.savedir,PACAKAGE)
        savePath = os.path.join(r'C:\Users\wujz\Desktop',PACAKAGE)
        logPath = os.path.join(savePath,LOG_DIR_NAME)
        os.mkdir(savePath)
        os.mkdir(logPath)
        
        mainLogger = Logger(os.path.join(logPath,LOG_NAME),'mainLogger')
        
        try:
            mainLogger.info("Main Scrit start ... ")
            
            # create index for extension
            mainLogger.info("'CreateExtensionIndex start...")
            ext_path = createExtensionIndex(savePath, 'stats') 
            print(ext_path)
            mainLogger.info("'CreateExtensionIndex complete...")
            
            # create thread to get index for license
            mainLogger.info("'CreateLicenseIndex thread start...")
            runCreateLicenseIndex = runScriptThread(createLicenseIndex, savePath, 'stats', ext_path)
            runCreateLicenseIndex.setDaemon(True)
            runCreateLicenseIndex.start()

            
            # create thread to get index for language
            mainLogger.info("CreateLangIndex thread start ...")
            runCreateLangIndex = runScriptThread(createLangIndex, savePath, 'stats', ext_path)
            runCreateLangIndex.setDaemon(True)
            runCreateLangIndex.start()
            
            runCreateLicenseIndex.join()
            runCreateLangIndex.join()
            mainLogger.info("'CreateLicenseIndex thread complete...")
            mainLogger.info("'CreateLangIndex thread complete...")
            
            # start to compress files to ZIP
            if not runCreateLangIndex.isAlive() and not runCreateLicenseIndex.isAlive():
                mainLogger.info("Start to compress files into package ...")
                print(os.listdir(savePath))
                zippath = r'C:\Users\wujz\Desktop\Package\{0}'.format(ZIP_NAME.format('Statistics'))
                destZip = zipfile.ZipFile(zippath, "w")  
                filelist = os.listdir(savePath)
                for file in filelist:
                    if zippath!=os.path.join(savePath,file) and file!=LOG_DIR_NAME:
                        destZip.write(os.path.join(savePath,file),file)
                destZip.close()
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
        print("Need permission to create folder in "+r'C:\Users\Jia Zhong\Desktop'+" or the destination already contains a folder named '"+PACAKAGE+"'")        