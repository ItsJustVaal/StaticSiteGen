class HTMLNode:
    def __init__(self, tag:str=None, value:str=None, children=None, props:dict=None) -> None: # type: ignore
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        temp = ''
        for k,v in self.props.items():
            temp += f' {k}="{v}"'
        return temp
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None) -> None: # type: ignore
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None and self.tag not in {"img", "br", "hr", "input", "meta", "link"}:
            raise ValueError("All LeafNodes must have a value, unless they're a void element")

        if self.tag is None:
            return self.value

        props = self.props_to_html() if self.props else ""

        # Void elements (no closing tag)
        if self.tag in {"img", "br", "hr", "input", "meta", "link"}:
            return f"<{self.tag}{props} />"

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

        
        
        
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children, props: dict = None) -> None: # type: ignore
        super().__init__(tag, None, children, props) # type: ignore
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("All ParentNodes must have a tag")
        if self.children is None:
            raise ValueError("All ParentNodes require children")
        res = f"<{self.tag}>"
        for child in self.children:
            res += child.to_html()
        res += f"</{self.tag}>"
        return res