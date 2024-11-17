def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    trimmed_blocks = [block.strip() for block in markdown_blocks if block.strip()]
         
    return trimmed_blocks