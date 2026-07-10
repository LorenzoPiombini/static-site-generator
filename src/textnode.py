from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
class TextNode:
    def __init__(self,text: str ,text_type: TextType ,url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url 

    def __eq__(self,other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url 
        
    def __repr__(self):
        if self.url is None:
            return f"TextNode({self.text}, {self.text_type.value})"
        else:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    try:
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None,text_node.text)
        if text_node.text_type == TextType.BOLD:
            return LeafNode("b",text_node.text)
        if text_node.text_type == TextType.ITALIC:
            return LeafNode("i",text_node.text)
        if text_node.text_type == TextType.CODE:
            return LeafNode("code",text_node.text)
        if text_node.text_type == TextType.LINK:
            return LeafNode("a",text_node.text,{"href":f'{text_node.url}'})
        if text_node.text_type == TextType.IMAGE:
            return LeafNode("img",None,{"src":f'{text_node.url}',"alt":f'{text_node.text}'})

    except AttributeError as e:
        raise ValueError(e)

