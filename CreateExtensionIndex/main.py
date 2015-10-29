'''
Created on Oct 27, 2015

@author: wujz
'''
from CreateExtensionIndex.CreateExtensionIndex import createExtensionIndex
from optparse import OptionParser 
import os

if __name__ == '__main__':    
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage)  
    parser.add_option("-o", "--output", dest="outdir", action='store', help="Choose a dir to save index file.")
    parser.add_option("-p", "--product", dest="productName", action='store', help="Choose index for which product: 1. SPSS Modeler 2. SPSS Statistics.")
    (options, args) = parser.parse_args() 

    if not os.path.isdir():
        parser.error("Please input a valid directory to create index file.")   
    if options.productName != "modeler" and options.productName != "stats":  
        parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
    
    try:
        createExtensionIndex(options.outdir, options.productName)
    except IOError as e:
        print(str(e))
    except Exception as e:
        print(str(e)) 