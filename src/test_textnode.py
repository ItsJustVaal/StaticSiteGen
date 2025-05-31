import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("URL Test", TextType.CODE)
        node2 = TextNode("URL Test", TextType.CODE, "OJAP.com")
        self.assertIsNone(node.URL)
        self.assertIsNotNone(node2.URL)

    def test_type(self):
        node = TextNode("URL Test", TextType.CODE)
        node2 = TextNode("URL Test", TextType.BOLD)
        node3 = TextNode("URL Test", TextType.IMAGE)
        self.assertEqual(node.text_type.value, "code")
        self.assertEqual(node2.text_type.value, "bold")
        self.assertEqual(node3.text_type.value, "image")



if __name__ == "__main__":
    unittest.main()