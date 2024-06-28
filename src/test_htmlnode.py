import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode("div","Hello, world!",None,{"class": "greeting", "href": "https://boot.dev"},)
        self.assertEqual(node.props_to_html(),' class="greeting" href="https://boot.dev"',)

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span","child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandhildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)
    
    def test_to_html_many_children(self):
        child1 = LeafNode("b","child1")
        child2 = LeafNode("i", 'child2')
        child3 = LeafNode("b", 'child3')
        parent_node = ParentNode("div",[child1,child2,child3])
        self.assertEqual(parent_node.to_html(),'<div><b>child1</b><i>child2</i><b>child3</b></div>')
    
    def test_headings(self):
        node = ParentNode("h2", [LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),])
        self.assertEqual(node.to_html(),"<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",)


if __name__ == "__main__":
    unittest.main()