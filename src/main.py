from textnode import TextNode, TextType


def main():
    node = TextNode("this is some dummy text", TextType.BOLD, URL="WOARO.com")
    print(node)
    
    
main()