""" GRaaS Views. """

import pkg_resources

from twisted.python.filepath import FilePath
from twisted.web.template import XMLString, Element, XMLFile, renderer


class MessageElement(Element):

    def __init__(self, text, message_type='info'):
        self._text = text
        self.loader = XMLString((
            '<div '
            'xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1"'
            ' class="alert alert-{}"><span t:render="text"></span>'
            '</div>'.format(message_type))
        )

    @renderer
    def text(self, request, tag):
        return self._text


class HomePageElement(Element):
    """ Home page template """
    static_path = pkg_resources.resource_filename(
        __name__, "static")
    loader = XMLFile(FilePath(static_path).child("index.xml"))

    def __init__(self, name, template=None, message='', message_type='info'):
        if template:
            self.loader = XMLFile(
                FilePath(self.static_path).child(template)
            )

        self._name = name
        self._message = message
        self._message_type = message_type

    @renderer
    def name(self, request, tag):
        return tag(self._name)

    @renderer
    def message(self, request, tag):
        return MessageElement(self._message, self._message_type)
