from copystructure import copy_structure
from generate import generate_pages_recursive


def main():
    copy_structure()
    generate_pages_recursive("content", "template.html", "public") 
    
    
main()