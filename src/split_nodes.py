from textnode import TextType, TextNode
from extract import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        substrings = old_node.text.split(delimiter)
        if len(substrings) % 2 == 0:
            raise Exception("Invalid Markdown syntax")
        for i in range(len(substrings)):
            if len(substrings[i]) == 0:
                continue
            node_text_type = text_type
            if i % 2 == 0:
                node_text_type = TextType.TEXT
            node = TextNode(substrings[i], node_text_type)
            new_nodes.append(node)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for text_node in old_nodes:
        if text_node.text_type != TextType.TEXT:
            new_nodes.append(text_node)
            continue
        text = text_node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
        last_text = ""
        for image_alt, image_link in images:
            last_text = ""
            arr = text.split(f"![{image_alt}]({image_link})", 1)
            if arr[0] != "":
                new_nodes.append(TextNode(arr[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if arr[1] != "":
                text = arr[1]
                last_text = text
        if last_text != "":
            new_nodes.append(TextNode(last_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for text_node in old_nodes:
        if text_node.text_type != TextType.TEXT:
            new_nodes.append(text_node)
            continue
        text = text_node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
        last_text = ""
        for alt_text, url in links:
            last_text = ""
            arr = text.split(f"[{alt_text}]({url})", 1)
            if arr[0] != "":
                new_nodes.append(TextNode(arr[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            if arr[1] != "":
                text = arr[1]
                last_text = text
        if last_text != "":
            new_nodes.append(TextNode(last_text, TextType.TEXT))

    return new_nodes


def split_nodes_all(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes
