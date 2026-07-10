



class HTMLNode:
    def __init__(self,tag: str | None = None,value: str | None = None, children: list['HTMLNode'] | None = None ,props: dict[str,str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("Not yet implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        result = " "
        for key,value in self.props.items():
            result = result + f"{key}=\"{value}\" "
        if result == " ":
            return result
        else:
            return result.rstrip()

class ParentNode(HTMLNode):
    def __init__(self,tag: str, children: list['HTMLNode'], props: dict[str,str] | None = None):
        super().__init__(tag=tag,children=children,props=props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Parent node must have a tag !!")  
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent node must have children !!")  
        html_str = f'<{self.tag}>'
        for c in self.children:
            html_str = html_str + c.to_html()
        html_str = html_str + f'</{self.tag}>'
        return html_str

        
class LeafNode(HTMLNode):
    def __init__(self,tag: str | None = None, value: str = "", props: dict[str,str] | None = None):
        super().__init__(tag=tag,value=value,children=None,props=props)
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        
        if self.tag != "img" and (self.value is None or self.value == ""):
            raise ValueError("a Leaf node must have a value !!")  
        if self.tag  is None:
            return f"{self.value}"
        if self.props is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            r = self.props_to_html()
            return f'<{self.tag}{r}>{self.value}</{self.tag}>'

            



