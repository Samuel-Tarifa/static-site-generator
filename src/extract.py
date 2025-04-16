import re


def extract_markdown_images(text):
    results = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return results


def extract_markdown_links(text):
    results = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return results

def extract_title(text):
    text=text.split('\n')
    for line in text:
        if line.startswith('# '):
            return line.removeprefix('# ')
    raise Exception('There must be a title in the markdown')
