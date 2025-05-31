import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("b", "This is some bold text", children=None, props={"href":"link.com", "target":"_blank"})
        self.assertEqual(node.props_to_html(), ' href="link.com" target="_blank"')

    def test_none(self):
        node = HTMLNode()
        node2 = HTMLNode("b", "test", [node], {"1":"2"})
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertIsNotNone(node2.tag)
        self.assertIsNotNone(node2.value)
        self.assertIsNotNone(node2.children)
        self.assertIsNotNone(node2.props)
        
    def test_repr(self):
        node = HTMLNode("b", "This is some bold text", children=None, props={"href":"link.com", "target":"_blank"})
        self.assertEqual(node.__repr__(), f"HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_with_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        
    def test_with_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")


class TestParentNode(unittest.TestCase):
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
    
    def test_no_tag(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode(None, [grandchild_node])  # type: ignore

        with self.assertRaises(ValueError) as context:
            child_node.to_html()

        self.assertEqual(str(context.exception), "All ParentNodes must have a tag")

class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_link_node(self):
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Google</a>')

    def test_bold_node(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")
    
    def test_image_node(self):
        node = TextNode("Alt description", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/image.png" alt="Alt description" />'
    )
        
    def test_invalid_text_type(self):
        class FakeType:
            pass
        node = TextNode("Oops", FakeType())  # type: ignore # Not a valid TextType
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Not a valid type")



if __name__ == "__main__":
    unittest.main()