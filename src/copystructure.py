import os
import shutil

def check_if_exists():
    #this isnt really needed but ensures fresh copy
    if os.path.exists("public"):
        shutil.rmtree("public")

def copy_structure():
    check_if_exists()
    
    shutil.copytree("static", "public")

