from markdown_to_html import markdown_to_html_node
from extract import extract_title
import os, shutil


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as file:
        text = file.read()
    with open(template_path, "r", encoding="utf-8") as html:
        template = html.read()

    html_body = markdown_to_html_node(text).to_html()
    html_title = extract_title(text)

    html = (
        template.replace("{{ Content }}", html_body)
        .replace("{{ Title }}", html_title)
        .replace('href="/', f'href="{base_path}')
        .replace('src="/', f'src="{base_path}')
    )

    parent_dirs = os.path.dirname(dest_path)
    os.makedirs(parent_dirs, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(html)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    def rec(path=""):
        parent = os.path.join(dir_path_content, path)
        for entry in os.listdir(parent):
            source_path = os.path.join(dir_path_content, path, entry)
            dst_path = os.path.join(dest_dir_path, path, entry)
            if os.path.isfile(source_path):
                html_filename = entry.removesuffix("md") + "html"
                dst = os.path.join(dest_dir_path, path, html_filename)
                generate_page(source_path, template_path, dst, base_path)
                print(f"copying {source_path} to {dst_path}")
            else:
                os.mkdir(dst_path)
                print(f"mkdir: {dst_path}")
                rec(os.path.join(path, entry))

    rec()
