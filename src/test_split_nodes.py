from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_all
from textnode import TextType, TextNode
import unittest


class test_split_nodes_delimeter(unittest.TestCase):
    def test_simple_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            repr(new_nodes),
            "[TextNode(This is text with a , text, None), TextNode(code block, code, None), TextNode( word, text, None)]",
        )

    def test_multiple_split(self):
        node = TextNode("lots of **big** and **bold** texts **really** ", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            repr(nodes),
            "[TextNode(lots of , text, None), TextNode(big, bold, None), TextNode( and , text, None), TextNode(bold, bold, None), TextNode( texts , text, None), TextNode(really, bold, None), TextNode( , text, None)]",
        )

    def test_multiple_delimeters(self):
        node = TextNode("This has **bold** and `code` and _italic_", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            repr(nodes),
            "[TextNode(This has , text, None), TextNode(bold, bold, None), TextNode( and , text, None), TextNode(code, code, None), TextNode( and , text, None), TextNode(italic, italic, None)]",
        )

    def test_no_delimiters(self):
        node = TextNode("This has no delimiters at all", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            repr(nodes), "[TextNode(This has no delimiters at all, text, None)]"
        )

    def test_unclosed_delimiter(self):
        node = TextNode("This has an *unclosed delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
            self.assertEqual(
                repr(nodes), "[TextNode(This has an *unclosed delimiter, text, None)]"
            )

    def test_empty_between_delimiters(self):
        node = TextNode("Some **** empty bold", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            repr(nodes),
            "[TextNode(Some , text, None), TextNode( empty bold, text, None)]",
        )

    def test_only_delimiters(self):
        node = TextNode("****", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(repr(nodes), "[]")

    def test_text_starts_with_delimiter(self):
        node = TextNode("**bold** and normal", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            repr(nodes),
            "[TextNode(bold, bold, None), TextNode( and normal, text, None)]",
        )

    def test_text_ends_with_delimiter(self):
        node = TextNode("normal and **bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            repr(nodes),
            "[TextNode(normal and , text, None), TextNode(bold, bold, None)]",
        )

    def test_multiple_adjacent_delimited(self):
        node = TextNode("**a****b****c**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            repr(nodes),
            "[TextNode(a, bold, None), TextNode(b, bold, None), TextNode(c, bold, None)]",
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_empty(self):
        node = TextNode("No images here!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("No images here!", TextType.TEXT)],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode("![alt](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    def test_split_images_image_at_end(self):
        node = TextNode(
            "Image at end ![end](https://example.com/end.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image at end ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_image_at_start(self):
        node = TextNode(
            "![start](https://example.com/start.png) text at end", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" text at end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("![one](url1)", TextType.TEXT),
            TextNode("and ![two](url2)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode("and ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
            ],
            new_nodes,
        )

    def test_split_nodes_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        results = split_nodes_all(text)
        self.assertListEqual(
            results,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_plain_text(self):
        text = "Just normal text"
        results = split_nodes_all(text)
        self.assertListEqual(results, [TextNode("Just normal text", TextType.TEXT)])

    def test_bold_and_italic(self):
        text = "**bold** and _italic_"
        results = split_nodes_all(text)
        self.assertListEqual(results, [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])

    def test_nested_markdown_not_supported(self):
        text = "**bold and _italic_**"
        results = split_nodes_all(text)
        self.assertListEqual(results, [
            TextNode("bold and _italic_", TextType.BOLD),
        ])

    def test_multiple_images(self):
        text = "Here is ![img1](url1) and ![img2](url2)"
        results = split_nodes_all(text)
        self.assertListEqual(results, [
            TextNode("Here is ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
        ])

    def test_multiple_links(self):
        text = "Links: [site1](url1), [site2](url2)"
        results = split_nodes_all(text)
        self.assertListEqual(results, [
            TextNode("Links: ", TextType.TEXT),
            TextNode("site1", TextType.LINK, "url1"),
            TextNode(", ", TextType.TEXT),
            TextNode("site2", TextType.LINK, "url2"),
        ])

    def test_unclosed_bold(self):
        text = "This is **broken markdown"
        with self.assertRaises(Exception):
            split_nodes_all(text)

    def test_empty_text(self):
        results = split_nodes_all("")
        self.assertListEqual(results, [])

    def test_code_inside_link(self):
        text = "Check [`code`](url)"
        results = split_nodes_all(text)
        self.assertListEqual(results, [
            TextNode("Check ", TextType.TEXT),
            TextNode("`code`", TextType.LINK, "url"),
        ])

    def test_text_after_image(self):
        text = "![alt](imgurl) then more text"
        results = split_nodes_all(text)
        self.assertListEqual(results, [
            TextNode("alt", TextType.IMAGE, "imgurl"),
            TextNode(" then more text", TextType.TEXT),
        ])

    def test_text_after_image(self):
        text = """This text
has 2 lines"""
        results = split_nodes_all(text)
        self.assertListEqual(results, [
            TextNode("This text\nhas 2 lines", TextType.TEXT),
        ])


if __name__ == "__main__":
    unittest.main()
