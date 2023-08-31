sanexml
==================
This repo is a pure python implementation for `lxml <https://github.com/lxml/lxml>`_.


Installation
-------------------

Requirements
###################
* Python 3.7 or later

.. code-block:: bash

    pip install sanexml

Documentation
---------------------------
sanexml is a fallback library for **lxml.etree** module, so the functions have same names and parameters.
This implementation is built on top of python's default xml library and BeautifulSoup4.

Below listed are the implemented functions.
###############################

* ``XMLParser``
* ``clear``
* ``remove_attribute``
* ``Comment``
* ``dump``
* ``Element``
* ``ElementTree``
* ``fromstring``
* ``indent``
* ``iselement``
* ``parse``
* ``strip_attributes``
* ``strip_elements``
* ``strip_tags``
* ``SubElement``
* ``tostringlist``
* ``tostring``
* ``XPath``

For documentation please refer to: https://lxml.de/tutorial.html