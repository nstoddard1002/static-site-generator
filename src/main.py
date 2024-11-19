from textnode import *
from htmlnode import *
from markdown import *
from fileops import *
from enum import Enum
import os
import shutil



def main():
	shutil.rmtree("public")
	copy_files_to_new_directory("static","public")
	generate_page("content/index.md","template.html","public")




if __name__ == "__main__":
	main()
