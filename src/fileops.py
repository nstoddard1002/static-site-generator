import os 
import shutil

def copy_static_to_public():

    #check if path "public" exists in working directory, and then delete its contents if so
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_files_to_new_directory("static","public")
    

def copy_files_to_new_directory(source, destination):
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
        
