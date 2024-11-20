from textnode import *
from htmlnode import *
from markdown import *
from fileops import *
from enum import Enum
import os
import shutil



def main():
	
	generate_pages_recursive("content","template.html","public")
	copy_static_to_public()




if __name__ == "__main__":
	main()
