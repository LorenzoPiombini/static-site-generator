import os
import shutil

WORKING_DIRECTORY = '/home/lpiombini/boot.dev/static-site-generator/'

def is_path_valid(working_directory: str ,path:str) -> bool:
        absolute_path = os.path.abspath(working_directory)
        built_path = os.path.join(absolute_path,path)
        target_dir = os.path.normpath(built_path)
        return os.path.commonpath([absolute_path,target_dir]) == absolute_path

def copy_file_over(src:str,dest:str):
    if os.path.isfile(src):
        shutil.copy(src,dest)
    else:
        # create the dir in dest if does not exist
        dir_at_dest = os.path.join(dest,os.path.basename(src))
        if os.path.exists(dir_at_dest) == False:
            os.mkdir(dir_at_dest)
        result = os.listdir(src)
        for r in result:
            src_p = os.path.join(src,r)
            copy_file_over(src_p,dir_at_dest)


def copy_content_to_folder(working: str, src:str,dest:str):
    try:
        if is_path_valid(working,dest) and is_path_valid(working,src):
            shutil.rmtree(dest)
            os.mkdir(dest)

            #list the direcotry content 
            content = os.listdir(src)
            for c in content:
                src_p = os.path.join(src,c)
                copy_file_over(src_p,dest)
    except Exception as e:
        print(e)
     
copy_content_to_folder(WORKING_DIRECTORY,"./static","./public")
