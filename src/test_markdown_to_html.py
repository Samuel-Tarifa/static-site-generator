import unittest
from markdown_to_html import markdown_to_html_node

class test_markdown_to_html(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "## This is a _heading_ with `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a <i>heading</i> with <code>code</code></h2></div>"
        )

    def test_quote_block(self):
        md = "> This is a quote\n> with **bold** and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> and <i>italic</i></blockquote></div>"
        )

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>"
        )

    def test_unordered_list(self):
        md = "- One\n- Two\n- Three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>One</li><li>Two</li><li>Three</li></ul></div>"
        )

    def test_mixed_blocks(self):
        md = """
# Title

This is a _paragraph_ with a [link](https://example.com) and `code`.

> A quote here

1. Item one
2. Item two

- Unordered one
- Unordered two

```
Code block here
```

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        text="<div><h1>Title</h1><p>This is a <i>paragraph</i> with a <a href=\"https://example.com\">link</a> and <code>code</code>.</p><blockquote>A quote here</blockquote><ol><li>Item one</li><li>Item two</li></ol><ul><li>Unordered one</li><li>Unordered two</li></ul><pre><code>Code block here\n</code></pre></div>"
        self.assertEqual(
            html,
            text
        )


if __name__ == '__main__':
    unittest.main()