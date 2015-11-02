'''
Created on Oct 27, 2015

@author: wujz
'''
from CreateLicenseIndex.createLicenseIndex import createLicenseIndex
from optparse import OptionParser 
import os

    
if __name__ == "__main__":    
    # usage = "usage: %prog [options] arg1 arg2 arg3"  
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage)  
    parser.add_option("-o", "--outdir", dest="outdir", action='store', help="Directory to save license index.")
    #parser.add_option("-p", "--product", dest="productName", action='store', help="Choose license index for which product: 1. modeler 2. stats.")
    parser.add_option("-e", "--extdir", dest="extdir", action='store', help="Directory to save extension index.")
    (options, args) = parser.parse_args() 
    
    # Currently this script is only used for stats
    #if options.productName.lower() != "modeler" and options.productName.lower() != "stats":   
    #    parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
        
    if not os.path.isdir(options.outdir):
        parser.error("Please input a valid directory to save license_index.json.")
        
    if not os.path.exists(options.extdir):
        parser.error("Please input a valid directory of extension index file.")
    
    try:
        createLicenseIndex(options.outdir, options.extdir)
    except IOError as e:
        print(str(e))
    except Exception as e:
        print(str(e))