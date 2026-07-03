from htmlnode import * 
from textnode import * 
from enum import Enum

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            result.append(n)
        else:
            if n.text.count(delimiter) == 0:
                result.append(n)
                continue
                #raise ValueError(f"delimiter '{delimiter}', not found!")
            if n.text.count(delimiter) < 2:
                raise ValueError(f"Missing closing delimiter for '{delimiter}'")

            splitted_text = n.text.split(delimiter)
            nodes = []
            for i in range(0,len(splitted_text)):
                if splitted_text[i] == "":
                    continue
                if i % 2 != 0:
                    if delimiter == '`':
                        nodes.append(TextNode(splitted_text[i],TextType.CODE,None))
                    if delimiter == '**':
                        nodes.append(TextNode(splitted_text[i],TextType.BOLD,None))
                    if delimiter == '_':
                        nodes.append(TextNode(splitted_text[i],TextType.ITALIC,None))
                else:
                        nodes.append(TextNode(splitted_text[i],TextType.TEXT,None))
                    
            result.extend(nodes);

    return result



