import re
from urllib.parse import urljoin
from xml.etree import ElementTree as ET


def relative_to_absolute(root, base_url):
    for element in root.iter():
        url = element.get('href')
        if url:
            absolute_url = urljoin(base_url, url)
            element.set('href', absolute_url)


class XMLParser(ET.XMLParser):
    def __init__(self, *, remove_comments=False, **kwargs):
        if not remove_comments:
            super().__init__()
        else:
            super().__init__(target=CommentedTreeBuilder())


def remove_attribute(element: ET.Element, attributes_to_delete):
    attributes = element.attrib
    for attribute in list(attributes):
        for del_attr in attributes_to_delete:
            if del_attr.match(attribute):
                attributes.pop(attribute)
                break


def Comment(text=None):
    """
    Comment(text=None)

        Comment element factory. This factory function creates a special element that will
        be serialized as an XML comment.
    """
    return ET.Comment(text=text)


class CommentedTreeBuilder(ET.TreeBuilder):
    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)


def dump(elem, pretty_print=True, with_tail=True):
    """
    dump(elem, pretty_print=True, with_tail=True)

        Writes an element tree or element structure to sys.stdout. This function
        should be used for debugging only.
    """
    if pretty_print:
        ET.indent(elem)
    ET.dump(elem=elem)


def Element(_tag, attrib=None, nsmap=None, **_extra):
    """
    Element(_tag, attrib=None, nsmap=None, **_extra)

        Element factory.  This function returns an object implementing the
        Element interface.

        Also look at the `_Element.makeelement()` and
        `_BaseParser.makeelement()` methods, which provide a faster way to
        create an Element within a specific document or parser context.
    """
    if nsmap:
        if type(nsmap) == dict:
            for key in nsmap:
                ET.register_namespace(key, nsmap[key])
        else:
            raise TypeError("nsmap should be type dictionary")
    # print("************************************")
    # print(_tag)
    # print("************************************")
    element = ET.Element(_tag, attrib or {}, **_extra)
    return element


def ElementTree(element=None, file=None, parser=None):
    """
    ElementTree(element=None, file=None, parser=None)

        ElementTree wrapper class.
    """
    if element is not None:
        return ET.ElementTree(element)
    elif file is not None:
        return ET.ElementTree().parse(source=file, parser=parser)
    else:
        return None


def fromstring(text, parser=None, base_url=None):
    """
    fromstring(text, parser=None, base_url=None)

        Parses an XML document or fragment from a string.  Returns the
        root node (or the result returned by a parser target).

        To override the default parser with a different parser you can pass it to
        the ``parser`` keyword argument.

        The ``base_url`` keyword argument allows to set the original base URL of
        the document to support relative Paths when looking up external entities
        (DTD, XInclude, ...).
    """
    print(text, "***********************************")
    root = ET.fromstring(text=text, parser=parser)
    if base_url:
        relative_to_absolute(root, base_url)
    return root


def indent(tree, space="  ", level=0):
    """
    indent(tree, space="  ", level=0)

        Indent an XML document by inserting newlines and indentation space
        after elements.

        *tree* is the ElementTree or Element to modify.  The (root) element
        itself will not be changed, but the tail text of all elements in its
        subtree will be adapted.

        *space* is the whitespace to insert for each indentation level, two
        space characters by default.

        *level* is the initial indentation level. Setting this to a higher
        value than 0 can be used for indenting subtrees that are more deeply
        nested inside of a document.
    """
    ET.indent(tree=tree, space=space, level=level)


def iselement(element):
    """
    iselement(element)

        Checks if an object appears to be a valid element object.
    """
    return ET.iselement(element)


def parse(source, parser=None, base_url=None):
    """
    parse(source, parser=None, base_url=None)

        Return an ElementTree object loaded with source elements.  If no parser
        is provided as second argument, the default parser is used.

        The ``source`` can be any of the following:

        - a file name/path
        - a file object
        - a file-like object
        - a URL using the HTTP or FTP protocol

        To parse from a string, use the ``fromstring()`` function instead.

        Note that it is generally faster to parse from a file path or URL
        than from an open file object or file-like object.  Transparent
        decompression from gzip compressed sources is supported (unless
        explicitly disabled in libxml2).

        The ``base_url`` keyword allows setting a URL for the document
        when parsing from a file-like object.  This is needed when looking
        up external entities (DTD, XInclude, ...) with relative paths.
    """
    element_tree = ET.parse(source=source, parser=parser)
    root = element_tree.getroot()
    if base_url:
        relative_to_absolute(root, base_url)
    return element_tree


def strip_attributes(tree_or_element, *attribute_names):
    """
    strip_attributes(tree_or_element, *attribute_names)

        Delete all attributes with the provided attribute names from an
        Element (or ElementTree) and its descendants.

        Attribute names can contain wildcards as in `_Element.iter`.

        Example usage::

            strip_attributes(root_element,
                             'simpleattr',
                             '{http://some/ns}attrname',
                             '{http://other/ns}*')
    """
    attributes_to_delete = []
    for attribute in attribute_names:
        attributes_to_delete.append(re.compile(attribute.replace("*", ".*")))

    if isinstance(tree_or_element, ET.Element):
        remove_attribute(element=tree_or_element, attributes_to_delete=attributes_to_delete)
    elif isinstance(tree_or_element, ET.ElementTree):
        for element in tree_or_element.iter():
            remove_attribute(element=element, attributes_to_delete=attributes_to_delete)
    else:
        raise TypeError(
            f"tree_or_element should be a type of Element or ElementTree, but found {type(tree_or_element)}")


def strip_elements(tree_or_element, *tag_names, with_tail=True):
    """
    strip_elements(tree_or_element, *tag_names, with_tail=True)

        Delete all elements with the provided tag names from a tree or
        subtree.  This will remove the elements and their entire subtree,
        including all their attributes, text content and descendants.  It
        will also remove the tail text of the element unless you
        explicitly set the ``with_tail`` keyword argument option to False.

        Tag names can contain wildcards as in `_Element.iter`.

        Note that this will not delete the element (or ElementTree root
        element) that you passed even if it matches.  It will only treat
        its descendants.  If you want to include the root element, check
        its tag name directly before even calling this function.

        Example usage::

            strip_elements(some_element,
                'simpletagname',             # non-namespaced tag
                '{http://some/ns}tagname',   # namespaced tag
                '{http://some/other/ns}*'    # any tag from a namespace
                lxml.etree.Comment           # comments
                )
    """
    if isinstance(tree_or_element, ET.ElementTree):
        root = tree_or_element.getroot()
    else:
        root = tree_or_element
    parent_map = {c: p for p in root.iter() for c in p}
    print(parent_map)
    for tag in tag_names:
        if type(tag) == str:
            elements_to_be_removed = root.findall(tag)
            for element_to_be_removed in elements_to_be_removed:
                if with_tail:
                    if element_to_be_removed.tail:
                        element_to_be_removed.tail = ""
                parent: ET.Element = parent_map[element_to_be_removed]
                parent.remove(element_to_be_removed)
        elif isinstance(tag, ET.Element):
            if tag == ET.Comment:
                for element in root.findall(".//"):
                    if element.tag == ET.Comment:
                        parent = parent_map[element]
                        parent.remove(element)


def strip_tags(tree_or_element, *tag_names):
    """
    strip_tags(tree_or_element, *tag_names)

        Delete all elements with the provided tag names from a tree or
        subtree.  This will remove the elements and their attributes, but
        *not* their text/tail content or descendants.  Instead, it will
        merge the text content and children of the element into its
        parent.

        Tag names can contain wildcards as in `_Element.iter`.

        Note that this will not delete the element (or ElementTree root
        element) that you passed even if it matches.  It will only treat
        its descendants.

        Example usage::

            strip_tags(some_element,
                'simpletagname',             # non-namespaced tag
                '{http://some/ns}tagname',   # namespaced tag
                '{http://some/other/ns}*'    # any tag from a namespace
                Comment                      # comments (including their text!)
                )
    """
    if isinstance(tree_or_element, ET.ElementTree):
        root = tree_or_element.getroot()
    else:
        root = tree_or_element
    tags_to_remove = dict()
    parent_map = {c: p for p in root.iter() for c in p}
    print(parent_map)
    # for tag in tag_names:
    #     if iselement(tag):
    #         if tag.tag == ET.Comment:
    #             tags_to_remove['Comment'] = 1
    #     else:
    #         tags_to_remove[tag] = 1
    # all_elements = root.findall(".//")
    # for element in all_elements:
    #     if element.tag in tags_to_remove:
    #         parent = element.find(f".//{element.tag}/..")
    for tag in tag_names:
        print(tag == ET.Comment)
        if tag == ET.Comment:
            for element in root.findall(".//"):
                if element.tag == ET.Comment:
                    parent = parent_map[element]
                    parent.remove(element)


def SubElement(_parent: ET.Element, _tag, attrib=None, nsmap=None, **_extra):
    """
    SubElement(_parent, _tag, attrib=None, nsmap=None, **_extra)

        Subelement factory.  This function creates an element instance, and
        appends it to an existing element.
    """
    new_element = Element(_tag=_tag, attrib=attrib, nsmap=nsmap, **_extra)
    _parent.append(new_element)
    return new_element


def tostringlist(element_or_tree, *args, **kwargs):
    """
    tostringlist(element_or_tree, *args, **kwargs)

        Serialize an element to an encoded string representation of its XML
        tree, stored in a list of partial strings.

        This is purely for ElementTree 1.3 compatibility.  The result is a
        single string wrapped in a list.
    """
    return ET.tostringlist(element_or_tree, *args, **kwargs)


def tostring(element_or_tree, method=None, encoding=None, pretty_print=False):
    if pretty_print:
        ET.indent(element_or_tree)
    return ET.tostring(element_or_tree, encoding, method)
