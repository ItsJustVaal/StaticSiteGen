import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        
        def test_markdown_to_block_switched(self):
            md = """
This has a `code` block

- This is
- a list
- in the middle

This has a trailing
paragraph with ![some text](here.com)
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This has a `code` block",
                    "- This is\n- a list\n- in the middle",
                    "This has a trailing\nparagraph with ![some text](here.com)"
                ]
            )
        
        def test_block_to_block_types(self):
            block = "# heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
            block = "```\ncode\n```"
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
            block = "> quote\n> more quote"
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
            block = "- list\n- items"
            self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
            block = "1. list\n2. items"
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
            block = "paragraph"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
            block = ". list\n2. items"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
            block = "> quote\nnot a quote"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
            block = "```\nnot code\n"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)