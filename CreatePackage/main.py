'''
Created on Oct 22, 2015

@author: wujz
'''
from optparse import OptionParser 
from common.Logger import Logger
from common.runScriptThread import runScriptThread
from CreateLicenseIndex.CreateLicenseIndex import createLicenseIndex 
from CreateExtensionIndex.CreateExtensionIndex import createExtensionIndex 
import os

PACAKAGE = "package"
LOG_NAME = 'main.log'
 
if __name__ == '__main__':
    usage = "usage: %prog [options] arg1"  
    parser = OptionParser(usage)  
    parser.add_option("-s", "--savedir", dest="savedir", action='store', help="Directory to save Statistics.zip")
    parser.add_option("-p", "--product", dest="productName", action='store', help="Choose license index for which product: 1. modeler 2. stats.")
    (options, args) = parser.parse_args() 
    
    if not os.path.isdir(options.savedir):
        parser.error("Please input a valid directory to save package.")
    if options.productName != "modeler" and options.productName != "stats":  
        parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
    
    try: 
        savePath = os.path.join(options.savedir,PACAKAGE)
        os.mkdir(savePath)
        mainLogger = Logger(os.path.join(savePath,LOG_NAME),'mainLogger')
        
        try:
            mainLogger.info("Main Scrit start ... ")
            
            # create index for extension
            mainLogger.info("'CreateExtensionIndex start...")
            createExtensionIndex(savePath, 'stats') 
            mainLogger.info("'CreateExtensionIndex complete...")
            
            # create thread to get index for license
            mainLogger.info("'CreateLicenseIndex' thread start...")
            runCreateLicenseIndex = runScriptThread(savePath, createLicenseIndex, savePath, 'stats')
            runCreateLicenseIndex.start()
            mainLogger.info("'CreateLicenseIndex' thread complete...")
            
        except Exception as e:
            mainLogger.error(str(e),e)
            raise e  
        finally:
            mainLogger.close()      
    except Exception as e:
        print(str(e))
    except IOError:
        print("Need permission to create folder in "+options.savedir+" or the destination already contains a folder named '"+PACAKAGE+"'")     
        

    
    
    
    
    
    