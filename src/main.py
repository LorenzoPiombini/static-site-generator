from textnode import *
from functions import *
from page_generator import *
import sys

def main():
    basepath = ""
    if len(sys.argv) <= 1:
        basepath = '/'
    else:
        basepath = sys.argv[1]

    
    copy_content_to_folder(WORKING_DIRECTORY,'static','./docs')
    generate_pages_recursive(WORKING_DIRECTORY,"./content","./template.html",'./docs',basepath)
    

if __name__ == "__main__":
    main()
