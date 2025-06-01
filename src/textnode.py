from enum import Enum
from pydoc import text

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "itelic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    

class TextNode:
    def __init__(self, text, text_type:TextType, URL=None) -> None:
        self.text = text
        self.text_type = text_type
        self.URL = URL
        
    def __eq__(self, node) -> bool: # type: ignore
        return self.text == node.text and self.text_type == node.text_type and self.URL == node.URL
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.URL})"


    
def text_node_to_html_node(text_node:TextNode):
    if text_node.text_type not in TextType:
        raise Exception("Not a valid type")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text) # type: ignore
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.URL})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.URL, "alt": text_node.text})
        
        
    