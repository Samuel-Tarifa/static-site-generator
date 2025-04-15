from htmlnode import HTMLNode, LeafNode,ParentNode
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_repr1(self):
        node = HTMLNode(tag="div", value="this is a div", props={"color": "red"})
        self.assertEqual(repr(node), 'HTMLNode(div, this is a div, None,  color="red")')

    def test_repr2(self):
        node = HTMLNode(
            tag="div", value="this is a div", children=[], props={"color": "red"}
        )
        self.assertEqual(repr(node), 'HTMLNode(div, this is a div, [],  color="red")')

    def test_repr2(self):
        child = HTMLNode(tag="li", props={}, value="this is a li")
        node = HTMLNode(
            tag="ul", value="this is a ul", children=[child], props={"color": "red"}
        )
        self.assertEqual(
            repr(node),
            'HTMLNode(ul, this is a ul, [HTMLNode(li, this is a li, None, None)],  color="red")',
        )

    def test_leaf_to_html_a(self):
        link = LeafNode("a", "This is a link", {"href": "https://boot.dev"})
        self.assertEqual(link.to_html(),'<a href="https://boot.dev">This is a link</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_tag_error(self):
        child_node=LeafNode('p','child')
        with self.assertRaises(ValueError):
            parent_node = ParentNode(None, [child_node])
            parent_node.to_html()

    def test_parent_node_tag_error(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode('p', [])
            parent_node.to_html()

    def test_parent_node_with_many_children(self):
        li_children=[]
        for i in range(0,3):
            li_child=LeafNode('li',f'li{i}')
            li_children.append(li_child)
        child_ul=ParentNode('ul',li_children,{'id':'ul'})
        child_p=LeafNode('p','other p',{'class':'text'})
        parent=ParentNode('div',[child_ul,child_p],{'color':'red'})

        html_expected='<div color="red"><ul id="ul"><li>li0</li><li>li1</li><li>li2</li></ul><p class="text">other p</p></div>'

        self.assertEqual(parent.to_html(),html_expected)

if __name__ == "__main__":
    unittest.main()
