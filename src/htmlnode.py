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
        for k,v in self.props.items():
            html_string = html_string  + " " + str(k) +"="+str(v)
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
        super().__init__(tag=tag, value=value,props=props or {})
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return str(self.value)
        html_string = "<" + str(self.tag)
        if self.props:
            for k,v in self.props.items():
                html_string = html_string + " " + str(k) + "=\"" + str(v) + "\""
        html_string = html_string + ">" + str(self.value) + "</" + str(self.tag) + ">"
        return html_string
