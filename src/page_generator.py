import os
from extract_markdown import *
from functions import *

def generate_page(from_path,template_path,dest_path):
    print(f"Generating from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path,"r") as m:
        markdown = m.read()
        m.close()
    template_html = ""
    with open(template_path,"r") as tmpl:
        template_html = tmpl.read()
        tmpl.close()
    page = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    p = template_html.replace("{{ Title }}",title)
    p = p.replace("{{ Content }}",page)
    with open(dest_path,"w") as index:
        index.write(p)
        index.close()

def gen_pages(from_path:str,temp:str,dest:str):
    for d in os.listdir(from_path):
        path = os.path.join(from_path,d)
        if os.path.isfile(path):
            base = os.path.basename(path)
            base = base[:-2]
            dest_final_path = f"{dest}/{base}html"
            generate_page(path,temp,dest_final_path)
        else:
            dest_dir = os.path.join(dest,d)
            if os.path.exists(dest_dir) == False:
                os.mkdir(dest_dir)
            gen_pages(path,temp,dest_dir)

def generate_pages_recursive(working:str,dir_path_content:str, template_path:str, dest_dir_path:str):
    try:
        if is_path_valid(working,dir_path_content) and is_path_valid(working,dir_path_content) and is_path_valid(working,template_path) and is_path_valid(working,dest_dir_path):
            gen_pages(dir_path_content,template_path,dest_dir_path) 

    except Exception as e:
        print(e)

