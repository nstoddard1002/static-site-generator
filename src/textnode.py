from enum import Enum

class TextType(Enum):
    NORMAL = "Normal text"
    BOLD = "Bold text"
    ITALIC = "Italic text"
    CODE = "Code text"
    LINK = "Link text"
    IMAGE = "Image text"

class TextNode(text, text_type,url=None):
    self.text = text
    self.text_type = text_type
    self.url = url

    def __eg__(self,other_text):
        if (self.text_type == other_text.text_type) and (self.text == other_text.text) and (self.url == other_text.url):
            return True
        return False
    
    def __repr__(self):
        new_string = "TextNode(" + str(text) +", "+str(self.text_type)+", "+str(url)")"
        return new_string
    
