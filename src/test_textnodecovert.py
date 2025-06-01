import unittest
from convert import extract_markdown_images, split_node_images, split_nodes_delimiter, text_to_textnodes
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

class TestImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)   
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_node_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_single_image_middle(self):
        input_node = TextNode("Some ![alt](img.jpg) text", TextType.TEXT)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, URL="img.jpg"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(split_node_images([input_node]), expected)

    def test_multiple_images(self):
        input_node = TextNode("A ![cat](cat.png) and ![dog](dog.jpg)", TextType.TEXT)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, URL="cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, URL="dog.jpg"),
        ]
        self.assertListEqual(split_node_images([input_node]), expected)

    def test_text_without_images(self):
        input_node = TextNode("Just a paragraph.", TextType.TEXT)
        expected = [input_node]
        self.assertListEqual(split_node_images([input_node]), expected)

    def test_non_text_node_passthrough(self):
        input_node = TextNode("![not text]", TextType.CODE)
        expected = [input_node]
        self.assertListEqual(split_node_images([input_node]), expected)
        
        
class TestFinalConvert(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)
        
    def test_plain_text_only(self):
        text = "Just a normal sentence with no formatting."
        expected = [TextNode(text, TextType.TEXT)]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_only_code_and_image(self):
        text = "`print()` is useful. Here's a ![cat](cat.jpg)"
        expected = [
            TextNode("print()", TextType.CODE),
            TextNode(" is useful. Here's a ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, URL="cat.jpg")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)