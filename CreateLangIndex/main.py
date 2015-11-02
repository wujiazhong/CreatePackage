'''
Created on Oct 28, 2015

@author: wujz
'''
from CreateLangIndex.createLangIndex import createLangIndex
from optparse import OptionParser 
import os
def utest():
    base = r'C:\Users\wujz\Desktop\Package'
    createLangIndex(base, 'stats', os.path.join(base, 'index_for_stats.json'))
    
if __name__ == '__main__':    
    # usage = "usage: %prog [options] arg1 arg2 arg3"  
    usage = "usage: %prog [options] arg1 arg2" 
    parser = OptionParser(usage)  
    parser.add_option("-o", "--output", dest="outdir", action='store', help="Choose a dir to save index file.")
    #parser.add_option("-p", "--product", dest="productName", action='store', help="Choose index for which product: 1. SPSS Modeler 2. SPSS Statistics.")
    parser.add_option("-e", "--extdir", dest="extdir", action='store', help="Directory to save extension index.")
    (options, args) = parser.parse_args() 

    if not os.path.isdir():
        parser.error("Please input a valid directory to create index file.")   
    # Currently this script is only used for stats
    #if options.productName.lower() != "modeler" and options.productName.lower() != "stats":  
    #    parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
    if not os.path.exists(options.extdir):
        parser.error("Please input a valid directory of extension index file.")
    
    try:
        createLangIndex(options.outdir, options.extdir)
    except IOError as e:
        print(str(e))
    except Exception as e:
        print(str(e)) 
    
    # utest()    
        