from copystructure import copy_structure
from generate import generate_pages_recursive
import sys

def main():
    basepath = sys.argv[1]
    
    copy_structure()
    generate_pages_recursive("content", "template.html", "docs", basepath) 
    
    
main()