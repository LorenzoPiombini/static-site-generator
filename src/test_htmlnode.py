import unittest
from htmlnode import *


class TestHTMLnode(unittest.TestCase):
    def test_props_to_html_empty_str(self):
        node = HTMLNode("p","this is a paragraph",[],{})
        r = node.props_to_html()
        self.assertEqual(r," ")

    def test_props_to_html(self):
        node = HTMLNode("a","this is a link",[],{"href":"https://lorenzopiombini.com","target":"_blank"})
        r = node.props_to_html()
        self.assertEqual(r," href=\"https://lorenzopiombini.com\" target=\"_blank\" ")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    #ParentNode test
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )

if __name__ == "__main__":
    unittest.main()
