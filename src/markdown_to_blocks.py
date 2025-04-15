from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip() != ""]
    return blocks


def block_to_block_type(block: str):
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1

    if i > 0 and i <= 6 and block[i] == " ":
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    block = block.split("\n")
    isQuote = True
    for line in block:
        if not line.startswith("> "):
            isQuote = False
    if isQuote:
        return BlockType.QUOTE

    isUnordered = True
    for line in block:
        if not line.startswith("- "):
            isUnordered = False
    if isUnordered:
        return BlockType.UNORDERED_LIST

    isOrdered = True
    for i in range(len(block)):
        if not block[i].startswith(f"{i+1}. "):
            isOrdered = False

    if isOrdered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
