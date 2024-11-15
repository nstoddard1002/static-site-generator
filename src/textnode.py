from enum import Enum

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
        if (self.text_type == other_text.text_type) and (self.text == other_text.text) and (self.url == other_text.url):
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



