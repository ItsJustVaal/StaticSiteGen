from enum import Enum

from convert import text_to_textnodes
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote' 
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'


def markdown_to_blocks(markdown:str):
    block = []
    for item in markdown.split("\n\n"):
        if item == "":
            continue
        block.append(item.strip())
    return block


def block_to_block_type(block:str):
    lines = block.split("\n")
    
    if block.startswith(("# ", "## ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html = block_to_html_node(block)
        children.append(html)
    return ParentNode("div", children, None) # type: ignore
    
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html(block)
    if block_type == BlockType.HEADING:
        return heading_to_html(block)
    if block_type == BlockType.CODE:
        return code_to_html(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html(block)
    raise ValueError("Invalid block type")
    
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html = text_node_to_html_node(node)
        children.append(html)
    return children

def paragraph_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html(block):
    tier = 0
    for char in block:
        if char == "#":
            tier += 1
        else:
            break
    if tier + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {tier}")
    text = block[tier + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{tier}", children)

def code_to_html(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    raw_text = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html(block):
    items = block.split("\n")
    html = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html.append(ParentNode("li", children))
    return ParentNode("ol", html)

def ulist_to_html(block):
    items = block.split("\n")
    html = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html.append(ParentNode("li", children))
    return ParentNode("ul", html)

def quote_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)