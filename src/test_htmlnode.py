import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a","link text",[],{"href": "http://links.com"})
        node2 = HTMLNode("a","link text",[],{"href": "http://links.com"})
        self.assertEqual(node,node2)
    
    def test_neq(self):
        node3 = HTMLNode("a","link text",[],{"href": "http://links.com"})
        node4 = HTMLNode("p","this is a paragraph",['DummyLink','DummyImage'],{})
        self.assertNotEqual(node3,node4)
    
    def test_html_properties(self):
        rubric_string = " href=http://google.com"
        test_HTML = HTMLNode("a","link",[],{"href":"http://google.com"})
        test_str = str(test_HTML.props_to_html())
        self.assertEqual(test_str,rubric_string)
    
    def test_leaf_properties(self):
        rubric_string = "<p>This is a paragraph of text</p>"
        test_leaf = LeafNode("p","This is a paragraph of text")
        test_string = str(test_leaf.to_html())
        self.assertEqual(test_string,rubric_string)

    def test_leaf_properties1(self):
        rubric_string = "<a href=\"https://google.com\">Click me!</a>"
        test_leaf = LeafNode("a","Click me!",{"href":"https://google.com"})
        test_string = str(test_leaf.to_html())
        self.assertEqual(test_string,rubric_string)

    def test_empty_leafnode(self):
        with self.assertRaises(ValueError):
            LeafNode("p") #no value provided, should raise Value Error

    #course material derived test
    def test_parent_properties(self):
        rubric_string = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        test_list = [LeafNode("b","Bold text"),LeafNode(None,"Normal text"),LeafNode("i","italic text"),LeafNode(None,"Normal text")]
        test_parent = ParentNode("p",test_list,)
        test_string = test_parent.to_html()
        self.assertEqual(test_string,rubric_string)

    def test_parent_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div",None) #no children, should raise ValueError
    
    def test_complex_nested_structure(self):
        #HTML Structure expected:
        #<div><p>This is normal paragraph text. <b>Bold text</b></p><span>Span text</span></div>
        inner_child_1 = LeafNode(tag=None,value="This is normal paragraph text. ")
        inner_child_2 = LeafNode("b","Bold text")
        inner_parent = ParentNode("p",[inner_child_1,inner_child_2])

        outer_child = LeafNode("span","Span text")
        test_parent = ParentNode("div",[inner_parent,outer_child])

        rubric_string = "<div><p>This is normal paragraph text. <b>Bold text</b></p><span>Span text</span></div>"
        self.assertEqual(test_parent.to_html(),rubric_string)

    def test_parent_properties_with_attributes(self):
        rubric_string = "<div class=\"container\" id=\"main\"><p>Content</p></div>"
        child = LeafNode("p", "Content")
        test_parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        self.assertEqual(test_parent.to_html(), rubric_string)
    


    

if __name__ == "__main__":
    unittest.main()

