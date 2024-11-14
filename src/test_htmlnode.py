import unittest
from htmlnode import HTMLNode

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


    

if __name__ == "__main__":
    unittest.main()
