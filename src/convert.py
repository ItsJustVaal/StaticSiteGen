from textnode import *
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts:list[str] = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
                
def extract_markdown_images(text):
    return list(re.findall(r"!\[(.*?)\]\((.*?)\)", text))

def extract_markdown_links(text: str):
    return list(re.findall(r"\[(.*?)\]\((.*?)\)", text))

def split_node_images(old_nodes: list[TextNode]):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        
        if not images:
            new_nodes.append(node)
            continue

        idx = 0  # pointer in the string

        for alt, url in images:
            # Build full image markdown pattern
            markdown = f"![{alt}]({url})"
            start = node.text.find(markdown, idx)

            if start == -1:
                continue

            # Add preceding text
            if start > idx:
                new_nodes.append(TextNode(node.text[idx:start], TextType.TEXT))

            # Add image node
            new_nodes.append(TextNode(alt, TextType.IMAGE, URL=url))

            idx = start + len(markdown)

        # Add remaining trailing text
        if idx < len(node.text):
            new_nodes.append(TextNode(node.text[idx:], TextType.TEXT))

    return new_nodes
        

def split_node_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        idx = 0
        for label, url in links:
            markdown = f"[{label}]({url})"
            start = node.text.find(markdown, idx)
            if start == -1:
                continue

            if start > idx:
                new_nodes.append(TextNode(node.text[idx:start], TextType.TEXT))
            new_nodes.append(TextNode(label, TextType.LINK, URL=url))
            idx = start + len(markdown)

        if idx < len(node.text):
            new_nodes.append(TextNode(node.text[idx:], TextType.TEXT))

    return new_nodes



def text_to_textnodes(text):
    nodes =[TextNode(text, TextType.TEXT)]
    
    nodes = split_node_images(nodes)
    nodes = split_node_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes
    
    