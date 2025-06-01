import unittest
from nested import split_nodes_delimiter
from textnode import TextNode, TextType

class TestConvertTextNode(unittest.TestCase):
    def test_split_simple_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result,expected)

    def test_split_multiple_codes(self):
        node = TextNode("Here is `code1` and `code2`", TextType.TEXT)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result,expected)

    def test_split_no_delimiters(self):
        node = TextNode("Just a normal sentence.", TextType.TEXT)
        expected = [node]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result,expected)
