class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_string = ""
        #insert the tag properties, if they exist
        if self.props:
            for k,v in self.props.items():
                html_string += f" {k}={v}"
        return html_string
    
    def __repr__(self):
        print(f"Tag: {self.tag}")
        print(f"Value: {self.value}")
        print(f"Children: {self.children}")
        print(f"Properties: {self.props}")
        new_string = "Tag: " +self.tag+ "\n Value: " + str(self.value) + "\n Children: "+str(self.children)+"\n Properties: "+str(self.props)
        return new_string

    def __eq__(self,Other_HTML):
        if self.tag == Other_HTML.tag:
            if self.value == Other_HTML.value:
                if self.children == Other_HTML.children:
                    if self.props == Other_HTML.props:
                        return True
        
        return False

class LeafNode(HTMLNode):
    def __init__(self,tag=None,value=None,props=None):
        # ensure that props is a dictionary even if none are passed
        super().__init__(tag=tag, value=value,props=props or {})
        #LeafNodes must have a value
        if self.value is None:
            raise ValueError("LeafNode must have a value")
    
    def to_html(self):
        #if no tag, just return the value
        if self.tag == None:
            return str(self.value)
        
        #open the tag
        html_string = f"<{self.tag}"
        #insert the tag properties, if they exist
        if self.props:
            for k,v in self.props.items():
                html_string += f" {k}=\"{v}\""
        #add the value to the string and close the tag
        html_string += f">{self.value}</{self.tag}>"
        return html_string

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        # ensure that props is a dictionary even if none are passed
        super().__init__(tag=tag,value=None,children=children,props=props or {})
        #ParentNode must have children
        if self.children is None:
            raise ValueError("ParentNode must have children")
        if not isinstance(self.children,list):
            raise TypeError("Children must be a list of HTML objects")

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        
        #open the tag
        html_string = f"<{self.tag}"
        
        #add properties if they exist
        if self.props:
            for k,v in self.props.items():
                html_string += f" {k}=\"{v}\""

        #close the tag
        html_string += ">"
        #generate HTML for each child element
        for child in self.children:
            html_string += child.to_html()
        html_string += "</" + str(self.tag) + ">"
        return html_string

