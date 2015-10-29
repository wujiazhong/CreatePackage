'''
Created on Oct 22, 2015

@author: wujz
'''
from common.Logger import Logger
from optparse import OptionParser 
from CreateLicenseIndex.executive import CreateLicenseIndex 
from CreateIndexForDownloadExtension.executive import CreateIndexForDownloadExtension 
import threading
import os,sys

PACAKAGE = "StatisticsZIP"
LOG_NAME = 'mainlog.txt'

class runScriptThread(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, file_path, funcName, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.funcName = funcName
        self.thread_stop = False
        self.file_path = file_path
 
    def run(self): #Overwrite run() method, put what you want the thread do here
        while not self.thread_stop:          
            self.funcName(*(self.args))
            
    def stop(self):
        self.thread_stop = True
 
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
        savePath = os.path.join(r'C:\Users\Jia Zhong\Desktop',PACAKAGE)
        os.mkdir(savePath)
        
        mainLogger = Logger(os.path.join(savePath,LOG_NAME),'mainLogger')
        
        try:
            mainLogger.info("Main Scrit start ... ")
            runCreateIndexForDownloadExtension = runScriptThread(savePath, CreateLicenseIndex.CreateIndex, savePath, 'stats')
            runCreateLicenseIndex = runScriptThread(savePath, CreateIndexForDownloadExtension.createIndex, savePath, 'stats')
            
            runCreateIndexForDownloadExtension.start()
            mainLogger.info("'CreateExtensionIndex' thread start...")
            
            runCreateLicenseIndex.start()
            mainLogger.info("'CreateLicenseIndex' thread start...")
            
            runCreateIndexForDownloadExtension.stop()
            mainLogger.info("'CreateExtensionIndex' thread complete...")
            runCreateLicenseIndex.stop()
            mainLogger.info("'CreateLicenseIndex' thread complete...")
        except Exception as e:
            mainLogger.error(str(e),e)
            raise e  
        finally:
            mainLogger.close()      
    except Exception as e:
        print(str(e))
    except IOError:
        print("Need permission to create folder in "+r'C:\Users\Jia Zhong\Desktop'+" or the destination already contains a folder named '"+PACAKAGE+"'")     
        