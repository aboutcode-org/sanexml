#
# Copyright (c) nexB Inc. and others. All rights reserved.
# sanexml is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/sanexml for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

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

    def test_strip_attributes(self):
        xml_string = '<root attr="value"><child attic="meow">text</child></root>'
        element1 = etree.fromstring(xml_string)
        element2 = etree.fromstring(xml_string)
        etree.strip_attributes(element1, 'attr')
        etree.strip_attributes(element2, 'att*')
        self.assertIsNone(element1.get('attr'))
        self.assertIsNone(element2.get('attr'))
        self.assertIsNone(element2.get('attic'))

    def test_strip_elements(self):
        xml_string = '<root><child><subchild/></child><close>LoremIpsum</close></root>'
        element = etree.fromstring(xml_string)
        etree.strip_elements(element, 'subchild')
        self.assertNotIn('subchild', [e.tag for e in element.iter()])

    def test_strip_tags(self):
        xml_string = '<root><!-- comment --><child>text</child></root>'
        element = etree.fromstring(xml_string)
        etree.strip_tags(element, etree.Comment)
        result = etree.tostring(element)
        self.assertEqual(result, b'<root><child>text</child></root>')
