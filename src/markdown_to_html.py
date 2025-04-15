from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from textnode import TextNode, TextType
from split_nodes import split_nodes_all
from text_to_html import text_node_to_html_node


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        child_node = block_to_htmlnodes(block, block_type)
        children.append(child_node)
    parent = ParentNode("div", children)
    return parent


def block_type_to_html_node(block_type, block):
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", [])
    if block_type == BlockType.CODE:
        return ParentNode("pre", [ParentNode("code", [])])
    if block_type == BlockType.HEADING:
        i = 0
        while i < len(block) and i < 6 and block[i] == "#":
            i += 1
        return ParentNode(f"h{i}", [])
    if block_type == BlockType.ORDERED_LIST:
        return ParentNode("ol", [])
    if block_type == BlockType.UNORDERED_LIST:
        return ParentNode("ul", [])
    if block_type == BlockType.QUOTE:
        return ParentNode("blockquote", [])


def block_to_htmlnodes(block, block_type):
    parent = block_type_to_html_node(block_type, block)

    if block_type == BlockType.PARAGRAPH:
        block = block.replace("\n", " ")
        nodes = split_nodes_all(block)
        for node in nodes:
            parent.children.append(text_node_to_html_node(node))

    if block_type == BlockType.CODE:
        block = block.removeprefix("```").removeprefix("\n").removesuffix("```")
        child = TextNode(block, TextType.TEXT)
        parent.children[0].children.append(text_node_to_html_node(child))

    if block_type == BlockType.HEADING:
        block = block.lstrip("# ")
        block = block.replace("\n", " ")
        nodes = split_nodes_all(block)
        for node in nodes:
            parent.children.append(text_node_to_html_node(node))

    if block_type == BlockType.ORDERED_LIST:
        block = block.split("\n")
        block_formatted = []
        for i in range(len(block)):
            block_formatted.append(block[i].removeprefix(f"{i+1}. "))

        for line in block_formatted:
            nodes = split_nodes_all(line)
            li = ParentNode("li", [])
            for node in nodes:
                li.children.append(text_node_to_html_node(node))
            parent.children.append(li)

    if block_type == BlockType.UNORDERED_LIST:
        block_formatted = []
        for line in block.split("\n"):
            block_formatted.append(line.removeprefix("- "))
        for line in block_formatted:
            li = ParentNode("li", [])
            nodes = split_nodes_all(line)
            for node in nodes:
                li.children.append(text_node_to_html_node(node))
            parent.children.append(li)

    if block_type == BlockType.QUOTE:
        block = block.split("\n")
        block_formatted = []
        for line in block:
            block_formatted.append(line.removeprefix("> "))
        block_formatted = " ".join(block_formatted)
        nodes = split_nodes_all(block_formatted)
        for node in nodes:
            parent.children.append(text_node_to_html_node(node))

    return parent
