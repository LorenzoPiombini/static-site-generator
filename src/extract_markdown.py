import re
from enum import Enum
from textnode import *
from htmlnode import *
from split_delimeter import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def extract_markdown_images(text: str) ->list[tuple[str,str]]: return re.findall(r"\!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text: str) -> list[tuple[str,str]] | None:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for old in old_nodes:
        if old.text == "" or old.text == None:
            continue
        if old.text_type != TextType.TEXT:
            result.append(old)
            continue;
        imgs = extract_markdown_images(old.text)
        if len(imgs) == 0:
            result.append(old)
        else:
            text = old.text
            for _ in range(0,len(imgs)): 
                before,after= text.split(f"![{imgs[_][0]}]({imgs[_][1]})",1)
                if before != "":
                    result.append(TextNode(before,TextType.TEXT))
                result.append(TextNode(imgs[_][0],TextType.IMAGE,imgs[_][1]))
                text = after
            if text != "":
                result.append(TextNode(text, TextType.TEXT))
    return result



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:               
    result = []
    for old in old_nodes:
        if old.text == "" or old.text == None:
            continue
        if old.text_type != TextType.TEXT:
            result.append(old)
            continue;
        links = extract_markdown_links(old.text)
        if len(links) == 0:
            result.append(old)
        else:
            text = old.text
            for _ in range(0,len(links)): 
                before,after = text.split(f"[{links[_][0]}]({links[_][1]})",1)
                if before != "":
                    result.append(TextNode(before,TextType.TEXT))
                result.append(TextNode(links[_][0],TextType.LINK,links[_][1]))
                text = after
            if text != "":
                result.append(TextNode(text, TextType.TEXT))
    return result

def text_to_textnodes(text):
    n = TextNode(text,TextType.TEXT)
    nodes = split_nodes_delimiter([n],"**",TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"_",TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    for i in range(0,len(blocks)):
        blocks[i] = blocks[i].strip()
    filtered = []
    for b in blocks:
        if b != "":
            filtered.append(b)
    return filtered
    


def block_to_block_type(block:str) -> BlockType:
    if block[0] == '#':
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith('```'):
        return BlockType.CODE
    if block[0] == ">" or block[0] == "> ":
        lines = block.split("\n")
        filtered = []
        for l in lines:
            if l != "":
                filtered.append(l)
        qcount = 0
        for f in filtered:
            if f.startswith(">") or f.endswith('> '):
                qcount += 1
        if qcount == len(filtered):
            return BlockType.QUOTE
    if block[0] == '-':
        lines = block.split("\n")
        filtered = []
        for l in lines:
            if l != "":
                filtered.append(l)
        ulcount = 0
        for f in filtered:
            if f.startswith("-"):
                ulcount += 1
        if ulcount == len(filtered):
            return BlockType.ULIST
    if block.startswith('1. '):
        lines = block.split("\n")
        filtered = []
        for l in lines:
            if l != "":
                filtered.append(l)
        olcount = 1 #we surely have one!
        start = int(block[0])
        for f in filtered:
            if re.match(r"^\d+\.\s",f):
                if int(f[0]) == start + 1:
                    olcount += 1
                    start = int(f[0])
        if olcount == len(filtered):
            return BlockType.OLIST
        
    return BlockType.PARAGRAPH

def text_to_children(block: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(block)
    res = []
    for n in nodes:
        res.append(text_node_to_html_node(n))
    return res

    

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for b in blocks:
        btype = block_to_block_type(b)
        if btype == BlockType.PARAGRAPH:
            sp = b.split('\n')
            data = " ".join(sp)
            children = text_to_children(data) 
            node = ParentNode("p",children)
            html_nodes.append(node)
            continue
        if btype == BlockType.HEADING:
            count = 0
            for c in b:
                if c == '#':
                    count += 1
                    continue
                break
            if count > 6:
                raise ValueError("Wrong sintax! More than 6 # in markdown file")

            sp = b.split('\n')
            data = " ".join(sp)
            children = text_to_children(data.replace("#","").lstrip());
            node = ParentNode(f"h{count}",children)
            html_nodes.append(node)
            continue
        if btype == BlockType.QUOTE:
            rp = b.replace(">","")
            sp = rp.split("\n")
            stripped = []
            for s in sp:
                if s != "":
                    stripped.append(s.strip())
            data = " ".join(stripped)
            children = text_to_children(data)
            node = ParentNode("blockquote",children)
            html_nodes.append(node)
            continue
        if btype == BlockType.ULIST:
            sp = b.split("\n")
            ul_kids = []
            for s in sp:
                if s == "":
                    continue
                line = s[2:]
                ul_kids.append(ParentNode("li",text_to_children(line)))
            node = ParentNode("ul",ul_kids)
            html_nodes.append(node)
            continue
        if btype == BlockType.OLIST:
            cl = re.sub(r"\d+\.\s","",b)
            sp = cl.split('\n')
            ol_kids = []
            for s in sp:
                ol_kids.append(ParentNode("li",text_to_children(s)))
            node = ParentNode("ol",ol_kids)
            html_nodes.append(node)
            continue

        rp = b.replace("```","").lstrip()
        html_nodes.append(ParentNode("pre",[text_node_to_html_node(TextNode(rp,TextType.CODE))]))

    parent_div = ParentNode("div",html_nodes)
    return parent_div

def extract_title(markdown: str):
    lines = markdown.split("\n")
    for l in lines:
        if l.count("#") == 1:
            return l.replace("#","").lstrip().rstrip()
    raise ValueError("there is not Title in this markdown")
    
    



