from copy_to_public import copy_statics
from generate_page import generate_page_recursive
import sys


def main():
    copy_statics('docs/')
    if len(sys.argv) > 1:
        base_path=sys.argv[1]
    else:
        base_path='/'
    generate_page_recursive('content/','template.html','docs/',base_path)

if __name__ == "__main__":
    main()
