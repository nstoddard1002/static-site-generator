import os 
import shutil
from htmlnode import *
from markdown import *
from textnode import *

def copy_static_to_public():
    copy_files_to_new_directory("static","public")
    

def copy_files_to_new_directory(source, destination):
    #check if path "public" exists in working directory, and then delete its contents if so
    #if os.path.exists(destination):
        #shutil.rmtree(destination)

    if not os.path.exists(destination): 
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

    new_document = template_content.replace("{{ Title }}", title_string).replace("{{ Content }}", content_string)

    os.makedirs(dest_path, exist_ok=True)

    base_name = os.path.basename(from_path)
    file_name_without_ext = os.path.splitext(base_name)[0]

    dest_file_path = os.path.join(dest_path,f"{file_name_without_ext}.html")
    with open(dest_file_path, "w") as file:
        file.write(new_document)


def generate_pages_recursive(content_dir, template_path, dest_dir_path):
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    
    os.makedirs(dest_dir_path, exist_ok=True)

    current_files = os.listdir(content_dir)
    for current_file in current_files:
        source_path = os.path.join(content_dir,current_file)

        if os.path.isfile(source_path):
            if current_file.endswith(".md"):
                generate_page(source_path, template_path, dest_dir_path)
            else:
                dest_file_path = os.path.join(dest_dir_path,current_file)
                shutil.copy(source_path,dest_file_path)
        elif os.path.isdir(source_path):
            new_dest_dir = os.path.join(dest_dir_path, current_file)
            generate_pages_recursive(source_path, template_path, new_dest_dir)
