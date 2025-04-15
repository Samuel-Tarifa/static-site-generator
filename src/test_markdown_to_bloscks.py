import unittest
from markdown_to_blocks import markdown_to_blocks,block_to_block_type,BlockType

class test_markdown_to_blocks(unittest.TestCase):

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

    def test_markdown_to_blocks_single_paragraph(self):
        text = "Este es un párrafo simple."
        result = markdown_to_blocks(text)
        self.assertEqual(result, ["Este es un párrafo simple."])

    def test_markdown_to_blocks_multiple_blocks(self):
        text = "Párrafo uno.\n\nPárrafo dos.\n\n# Encabezado\n\nOtro párrafo"
        result = markdown_to_blocks(text)
        self.assertEqual(result, [
            "Párrafo uno.",
            "Párrafo dos.",
            "# Encabezado",
            "Otro párrafo"
        ])

    def test_markdown_to_blocks_with_extra_spaces(self):
        text = "   Primer bloque.   \n\n\n\n    Segundo bloque   \n\n"
        result = markdown_to_blocks(text)
        self.assertEqual(result, [
            "Primer bloque.",
            "Segundo bloque"
        ])

    def test_markdown_to_blocks_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Título"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Subtítulo"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        code_block = "```\ndef hola():\n    print(\"Hola\")\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        quote = "> Esto es una cita\n> multilinea"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        lista = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(lista), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        lista = "1. Uno\n2. Dos\n3. Tres"
        self.assertEqual(block_to_block_type(lista), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        parrafo = "Este es un bloque normal de texto que no tiene formato especial."
        self.assertEqual(block_to_block_type(parrafo), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_invalid(self):
        self.assertEqual(block_to_block_type("####### No válido"), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_partial(self):
        block = "> Esto es una cita\nNo debería contar"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_partial(self):
        block = "- Item 1\nItem sin guion"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_wrong_numbering(self):
        block = "1. Uno\n2. Dos\n4. Cuatro"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == '__main__':
    unittest.main()