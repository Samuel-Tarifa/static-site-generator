from copy_to_public import copy_to_public
from generate_page import generate_page_recursive


def main():
    copy_to_public()
    generate_page_recursive('content/','template.html','public/')

if __name__ == "__main__":
    main()
