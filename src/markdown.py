from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
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
        return "quote"
    elif all(re.match(ulist_pattern, block_line) for block_line in block_lines):
        return "unordered list"
    elif all(re.match(olist_pattern, block_line) for block_line in block_lines):
        return "ordered list"
    else:
        return "paragraph"