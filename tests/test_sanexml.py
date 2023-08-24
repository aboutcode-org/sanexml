import unittest
from sanexml import etree


class TestSaneXMLEtreeMethods(unittest.TestCase):

    def test_fromstring(self):
        xml_string = '<root><child>text</child></root>'
        element = etree.fromstring(xml_string)
        self.assertEqual(element.tag, 'root')

    def test_tostring(self):
        xml_string = '<root><child>text</child></root>'
        element = etree.fromstring(xml_string)
        result = etree.tostring(element)
        self.assertEqual(result, bytes(xml_string, 'utf-8'))

    def test_Element(self):
        element = etree.Element('root')
        self.assertEqual(element.tag, 'root')

    def test_Subelement(self):
        parent = etree.Element('root')
        child = etree.SubElement(parent, 'child')
        self.assertEqual(parent[0], child)

    def test_indent(self):
        xml_string = '<root><child>text</child></root>'
        element = etree.fromstring(xml_string)
        etree.indent(element)
        expected_result = b'<root>\n  <child>text</child>\n</root>'
        result = etree.tostring(element)
        self.assertEqual(result, expected_result)

    def test_iselement(self):
        element = etree.Element('root')
        self.assertTrue(etree.iselement(element))
        self.assertFalse(etree.iselement('not an element'))

    # def test_strip_attributes(self):
    #     xml_string = '<root attr="value"><child>text</child></root>'
    #     element = etree.fromstring(xml_string)
    #     etree.strip_attributes(element, ['attr'])
    #     self.assertIsNone(element.get('attr'))

    def test_strip_elements(self):
        xml_string = '<root><child><subchild/></child></root>'
        element = etree.fromstring(xml_string)
        etree.strip_elements(element, 'subchild')
        self.assertNotIn('subchild', [e.tag for e in element.iter()])

    def test_strip_tags(self):
        xml_string = '<root><!-- comment --><child>text</child></root>'
        element = etree.fromstring(xml_string)
        etree.strip_tags(element, etree.Comment)
        result = etree.tostring(element)
        self.assertEqual(result, b'<root><child>text</child></root>')
