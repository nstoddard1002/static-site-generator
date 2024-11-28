from enum import Enum
import re 


class TextType(Enum):
    NORMAL = "Normal text"
    BOLD = "Bold text"
    ITALIC = "Italic text"
    CODE = "Code text"
    LINK = "Link text"
    IMAGE = "Image text"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,other_text):
        if self.text == other_text.text:
            if self.text_type == other_text.text_type:
                if self.url == other_text.url:
                    return True
        return False
    
    def __repr__(self):
        new_string = "TextNode(" + str(self.text) +", "+str(self.text_type)+", "+str(self.url) + ")"
        return new_string
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        remaining_text = old_node.text
        if len(remaining_text) > 0:
            current_type = old_node.text_type
            while delimiter in remaining_text:
                pre_text, _, post_text = remaining_text.partition(delimiter)
                if pre_text:
                    new_nodes.append(TextNode(pre_text,current_type))
                current_type = text_type
                remaining_text = post_text
                if not remaining_text:
                    current_type = old_node.text_type
                    break
            current_type = old_node.text_type
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, current_type))
        else:
            new_nodes.append(TextNode("",old_node.text_type)) 
    
    return new_nodes

def extract_markdown_images(text):
    image_list = []
    matches = re.findall(r"!\[([^[\]]*)\]\(([^\(\)]*)\)", text)
    for image_text, image_url in matches:
        image_tuple = (image_text, image_url)
        image_list.append(image_tuple)
    return image_list

def extract_markdown_links(text):
    link_list = []
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for link_text, link_url in matches:
        link_tuple = (link_text, link_url)
        link_list.append(link_tuple)
    return link_list

def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        node_images = extract_markdown_images(old_node.text)
        remaining_text = old_node.text
        
        for alt_text, image_url in node_images:
            full_image_syntax = f"![{alt_text}]({image_url})"
            before_image, _, after_image = remaining_text.partition(full_image_syntax)

            if before_image:
                new_nodes.append(TextNode(before_image, old_node.text_type))
            
            image_node = TextNode(alt_text, TextType.IMAGE, url=image_url)
            new_nodes.append(image_node)

            remaining_text = after_image
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, old_node.text_type))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        node_links = extract_markdown_links(old_node.text)
        remaining_text = old_node.text
 
        for link_text, link_url in node_links:
            full_link_syntax = f"[{link_text}]({link_url})"
            before_link, _, after_link = remaining_text.partition(full_link_syntax)

            if before_link:
                new_nodes.append(TextNode(before_link,old_node.text_type))

            new_nodes.append(TextNode(link_text,TextType.LINK,link_url))

            remaining_text = after_link

        if remaining_text:
            new_nodes.append(TextNode(remaining_text,old_node.text_type))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.NORMAL,url=None)]
    #process formatting delimiters
    nodes = split_nodes_delimiter(nodes,"**",TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"*",TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)

    #process images and links
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)

    #remove empty TextNode entries
    nodes = [node for node in nodes if node.text]
    return nodes

def extract_title(markdown):
    markdown_lines = markdown.split("\n")
    title_syntax = "#"
    for markdown_line in markdown_lines:
        if markdown_line[0] == title_syntax:
            return markdown_line.lstrip("# ")
    raise Exception("no h1 heading found")

