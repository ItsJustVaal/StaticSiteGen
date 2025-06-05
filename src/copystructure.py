import os
import shutil

def check_if_exists():
    #this isnt really needed but ensures fresh copy
    if os.path.exists("docs"):
        shutil.rmtree("docs")

def copy_structure():
    check_if_exists()
    
    shutil.copytree("static", "docs")

