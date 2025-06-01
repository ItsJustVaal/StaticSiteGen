from textnode import *

# def type_from_delimiter(text_type):
#     for delim in TextType:
#         print(text_type)
#         print(delim.value)
#         if delim.value == text_type:
#             return delim
#     return None

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
                
# node = TextNode("This is text with a `code block` word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

# print(new_nodes)                



# if arr[0] == '' node 1 is the block
# if arr[-1] == '' node[-2] is block
# else node[1] is block