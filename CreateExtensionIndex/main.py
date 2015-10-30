'''
Created on Oct 27, 2015

@author: wujz
'''
from CreateExtensionIndex.createExtensionIndex import createExtensionIndex
from optparse import OptionParser 
import os

if __name__ == '__main__':    
    #usage = "usage: %prog [options] arg1 arg2"  
    usage = "usage: %prog [options] arg1"
    parser = OptionParser(usage)  
    parser.add_option("-o", "--output", dest="outdir", action='store', help="Choose a dir to save index file.")
    #parser.add_option("-p", "--product", dest="productName", action='store', help="Choose index for which product: 1. SPSS Modeler 2. SPSS Statistics.")
    (options, args) = parser.parse_args() 

    if not os.path.isdir():
        parser.error("Please input a valid directory to create index file.")   
        
    # Currently this script is only used for stats
    # if options.productName.lower() != "modeler" and options.productName.lower() != "stats":  
    #     parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
    
    try:
        createExtensionIndex(options.outdir, 'stats')
    except IOError as e:
        print(str(e))
    except Exception as e:
        print(str(e)) 