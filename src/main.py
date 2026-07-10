from textnode import *
from functions import *
from page_generator import *

def main():
    copy_content_to_folder(WORKING_DIRECTORY,'./static','./public')
    generate_pages_recursive(WORKING_DIRECTORY,"./content","./template.html",'./public')
    

if __name__ == "__main__":
    main()
