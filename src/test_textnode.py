import unittest
from textnode import *
from split_delimeter import split_nodes_delimiter
from extract_markdown import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text_type(self): 
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self): 
        node = TextNode("This is a text node", TextType.BOLD,"http://lorenzopiombini.com")
        node2 = TextNode("This is a text node", TextType.BOLD,"http://softexample.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_str(self): 
        node = TextNode("This is a text Node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_str(self): 
        node = TextNode("This is a text Node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD,)
        self.assertNotEqual(node, node2)

    def test_not_eq_one_url_one_not(self): 
        node = TextNode("This is a text node", TextType.BOLD,"http://lorenzopiombini.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split(self):
        node = TextNode("This is text with a **bolded phrase** in the middle",TextType.TEXT)
        nodes = split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(len(nodes),3)
        self.assertEqual(nodes[1].text,"bolded phrase")
        self.assertEqual(nodes[1].text_type,TextType.BOLD)

    def test_split_2(self):
        node = TextNode("This is text with a bolded phrase at the **end**",TextType.TEXT)
        nodes = split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(len(nodes),2)
        self.assertEqual(nodes[1].text,"end")
        self.assertEqual(nodes[1].text_type,TextType.BOLD)

    def test_split_raise(self):
        node = TextNode("This is text with a bolded phrase at the **end",TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    #def test_split_raise_2(self):
    #    node = TextNode("This is text with a bolded phrase at the end, but no delimiter wathsoever",TextType.TEXT)
   #     with self.assertRaises(ValueError):
           # split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_code(self):
        node = TextNode("This is text with a `bolded phrase` in the middle",TextType.TEXT)
        nodes = split_nodes_delimiter([node],'`',TextType.CODE)
        self.assertEqual(len(nodes),3)
        self.assertEqual(nodes[1].text,"bolded phrase")
        self.assertEqual(nodes[1].text_type,TextType.CODE)

    def test_split_italic(self):
        node = TextNode("This is text with a _bolded phrase_ in the middle",TextType.TEXT)
        nodes = split_nodes_delimiter([node],'_',TextType.ITALIC)
        self.assertEqual(len(nodes),3)
        self.assertEqual(nodes[1].text,"bolded phrase")
        self.assertEqual(nodes[1].text_type,TextType.ITALIC)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_fail(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [example](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("example", "https://i.imgur.com/zjjcJKZ.png")], matches)

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

    def test_split_links(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
                )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                    )],
            new_nodes,
            )

    def test_text(self):
        t = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(t)
        self.assertListEqual(
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    ],
                new_nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

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

    def test_heading_levels(self):
        md = """
## This is an h2

### This is an h3

#### This is an h4
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is an h2</h2><h3>This is an h3</h3><h4>This is an h4</h4></div>",
        )

    def test_heading_with_inline(self):
        md = """
# This is **bold** in a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is <b>bold</b> in a heading</h1></div>",
        )

    def test_unordered_list_with_inline(self):
        md = """
- Item with **bold**
- Item with `code`
- Plain item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item with <b>bold</b></li><li>Item with <code>code</code></li><li>Plain item</li></ul></div>",
        )

    def test_ordered_list_with_inline(self):
        md = """
1. First with _italic_
2. Second item
3. Third with **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First with <i>italic</i></li><li>Second item</li><li>Third with <b>bold</b></li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Title

Some paragraph with **bold** and _italic_.

- list item one
- list item two

> A blockquote here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>Some paragraph with <b>bold</b> and <i>italic</i>.</p><ul><li>list item one</li><li>list item two</li></ul><blockquote>A blockquote here</blockquote></div>",
        )

if __name__ == "__main__":
    unittest.main()
