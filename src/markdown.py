from enum import Enum
import re
from textnode import *
from htmlnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "blockquote"
    ULIST = "unordered list"
    OLIST = "ordered list"

def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    trimmed_blocks = [block.strip() for block in markdown_blocks if block.strip()]
         
    return trimmed_blocks

def block_to_blocktype(block):
    block_lines = block.split("\n")

    heading_pattern = r"^#{1,6} "
    code_start_pattern = r"^```"
    code_end_pattern = r"```$"
    quote_pattern = r"^>"
    ulist_pattern = r"^[*-] "
    olist_pattern = r"^\d+\. "

    if len(block_lines) == 1 and re.match(heading_pattern, block_lines[0]):
        return "heading"
    elif re.match(code_start_pattern, block_lines[0]) and re.match(code_end_pattern, block_lines[-1]):
        return "code"
    elif all(re.match(quote_pattern, block_line) for block_line in block_lines):
        return "blockquote"
    elif all(re.match(ulist_pattern, block_line) for block_line in block_lines):
        return "unordered list"
    elif all(re.match(olist_pattern, block_line) for block_line in block_lines):
        return "ordered list"
    else:
        return "paragraph"

def markdown_to_HTMLNode(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_and_types = []
    for block in blocks:
        blocks_and_types.append(tuple((block_to_blocktype(block),block)))
    
    html_nodes = []
    for block_type, block in blocks_and_types:
        if block_type == "paragraph":
            new_nodes = text_to_textnodes(block)
            new_html_nodes = []
            for node in new_nodes:
                new_html_nodes.append(text_node_to_html_node(node))
            html_nodes.append(ParentNode("p",new_html_nodes))
        elif block_type == "heading":
            heading_level = 0
            for char in block:
                if char == "#":
                    heading_level += 1
                else:
                    break
            heading_tag = f"h{heading_level}"
            html_nodes.append(LeafNode(heading_tag,block[(heading_level+1):]))
        elif block_type == "code":
            code_lines = block.split("\n")[1:-1]
            code_content = "\n".join(code_lines)
            html_nodes.append(LeafNode("code",code_content))
        elif block_type == "blockquote":
            quote_content = " ".join(line.lstrip("> ") for line in block.split("\n"))
            html_nodes.append(LeafNode("blockquote",quote_content))
        elif block_type == "unordered list":
            list_items = []
            for line in block.split("\n"):
                list_item_text = line.lstrip("*- ")
                line_nodes = [text_node_to_html_node(node) for node in text_to_textnodes(list_item_text)]
                list_items.append(ParentNode("li",line_nodes))
            html_nodes.append(ParentNode("ul", list_items))
        elif block_type == "ordered list":
            list_items = []
            for line in block.split("\n"):
                prefix_index = line.find(".")
                list_item_text = line[prefix_index + 1:].strip()
                line_nodes = [text_node_to_html_node(node) for node in text_to_textnodes(list_item_text)]
                list_items.append(ParentNode("li", line_nodes))
            html_nodes.append(ParentNode("ol", list_items))
    return ParentNode("div",html_nodes)

            


