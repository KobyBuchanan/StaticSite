import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"



def markdown_to_block(markdown):
    blocks = markdown.split("\n\n")
    split_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        split_blocks.append(block)
    return split_blocks


def block_to_block_type(block:str):
    headings = ["# ", "## ", "### ","#### ","##### ","###### "]
    if block.startswith(tuple(headings)):
        return block_type_heading
    
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    
    if block.startswith(">"):
        for item in block.split("\n"):
            if not item.startswith(">"):
                return block_type_paragraph
            return block_type_quote
        
    if block.startswith("* "):
        for item in block.split("\n"):
            if not item.startswith("* "):
                return block_type_paragraph
            return block_type_unordered_list
        
    if block.startswith("- "):
        for item in block.split("\n"):
            if not item.startswith("- "):
                return block_type_paragraph
            return block_type_unordered_list
        
    if block.startswith("1. "):
        i = 1
        for item in block.split("\n"):
            if not item.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered_list
    
    return block_type_paragraph


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragragh_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html(block):
    pattern = r"(\#+ )(.*)"
    heading_text_tup = re.findall(pattern, block)[0]
    heading_num = len(heading_text_tup[0])-1
    tag = f"h{heading_num}"
    children = text_to_children(heading_text_tup[1])
    return ParentNode(tag, children)

def code_to_html(block):
    code = block.strip("```")
    children = text_to_children(code)
    code_node = ParentNode(block_type_code,children)
    return ParentNode("pre",[code_node])

def quote_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.strip(">"))
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragragh_to_html(block)
    if block_type == block_type_heading:
        return heading_to_html(block)
    if block_type == block_type_code:
        return code_to_html(block)
    if block_type == block_type_quote:
        return quote_to_html(block)
    if block_type == block_type_unordered_list:
        return ulist_to_html(block)
    if block_type == block_type_ordered_list:
        return olist_to_html(block)
    raise ValueError("Invalid block type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)