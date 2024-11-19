import os 
import shutil
from htmlnode import *
from markdown import *
from textnode import *

def copy_static_to_public():
    copy_files_to_new_directory("static","public")
    

def copy_files_to_new_directory(source, destination):
    #check if path "public" exists in working directory, and then delete its contents if so
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    current_files = os.listdir(source)
    for current_file in current_files:
        source_path = os.path.join(source,current_file)
        destination_path = os.path.join(destination,current_file)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        else:
            copy_files_to_new_directory(source_path, destination_path)

def generate_page(from_path,template_path,dest_path):
    if not os.path.exists(from_path):
        raise Exception("source file doesn't exist")
    elif not os.path.exists(template_path):
        raise Exception("template doesn't exist")
    

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        md_content = file.read()
    
    with open(template_path) as file:
        template_content = file.read()
    
    converted_content = markdown_to_HTMLNode(md_content)
    content_string = converted_content.to_html()
    title_string = extract_title(md_content)
    work_template = template_content.split("\n")
    new_document = []
    for work in work_template:
        if "{{ Title }}" in work:
            before_title, _, after_title = work.partition("{{ Title }}")
            new_document.append(before_title + title_string + after_title)
        elif "{{ Content }}" in work:
            before_content, _, after_content = work.partition("{{ Content }}")
            new_document.append(before_content + content_string + after_content)
        else:
            new_document.append(work)
    completed_html_string = "".join(new_document)

    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    
    file_name = os.path.join(dest_path,"index.html")
    with open(file_name, "w") as file:
        file.write(completed_html_string)


        
