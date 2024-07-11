import unittest

from block_markdown import (markdown_to_block,
                            block_to_block_type,
                            markdown_to_html_node,
                            block_type_paragraph,
                            block_type_heading,
                            block_type_code,
                            block_type_quote,
                            block_type_unordered_list,
                            block_type_ordered_list
                            )

class Testblock_markdown(unittest.TestCase):
    def test_markdown_to_block(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        mdtoblck = markdown_to_block(markdown)
        self.assertEqual(mdtoblck,['This is **bolded** paragraph', 
                                   'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line',
                                    '* This is a list\n* with items'])
        
    def test_block_to_block_type_paragrapgh(self):
        block  = "This is a test block paragragh"
        self.assertEqual(block_to_block_type(block),block_type_paragraph)

    def test_block_to_block_type_headings(self):
        heading_blocks  = ["# This is a h1 block",
                           "## This is a h2 block",
                           "### This is a h3 block",
                           "#### This is a h4 block",
                           "##### This is a h5 block",
                           "###### This is a h6 block",
                           ]
        for heading in heading_blocks:
            self.assertEqual(block_to_block_type(heading),block_type_heading)
        heading_fail_blocks  = ["#This is a h1 block",
                           "##This is a h2 block",
                           "###This is a h3 block",
                           "####This is a h4 block",
                           "#####This is a h5 block",
                           "######This is a h6 block",
                           "####### no 7?",
                           "nothing"
                           ]
        for heading in heading_fail_blocks:
            self.assertEqual(block_to_block_type(heading),block_type_paragraph)

    def test_markdown_paragragh_to_html_node(self):
        md = "This is a paragrapgh block. It only ccontains words and is a paragraghtype."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a paragrapgh block. It only ccontains words and is a paragraghtype.</p></div>")


    def test_markdown_heading_to_html_node(self):
        md = "### This is a heading 3 header!!"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is a heading 3 header!!</h3></div>")

    def test_markdown_code_to_html_node(self):
        md = "```This is a code block```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>This is a code block</code></pre></div>")

    def test_markdown_quote_to_html_node(self):
        md = ">Do not go gentle into that goodnight\n>Rage,rage against the dying of the light"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Do not go gentle into that goodnight Rage,rage against the dying of the light</blockquote></div>")

    def test_markdown_ulist_to_html_node(self):
        md = """
- this is item one
- item two
- item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>this is item one</li><li>item two</li><li>item 3</li></ul></div>")

    def test_markdown_0list_to_html_node(self):
        md = """
1. this is item one
2. item two
3. item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>this is item one</li><li>item two</li><li>item 3</li></ol></div>")


if __name__ == "__main__":
    unittest.main()