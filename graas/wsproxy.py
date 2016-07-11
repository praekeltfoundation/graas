""" Utilities for proxying requests to a real GRaaS server over a
    WebSocket.
    """

from autobahn.twisted.websocket import (
    WebSocketServerFactory, WebSocketServerProtocol)
from autobahn.twisted.resource import WebSocketResource


class GraasServerWsProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("WebSocket connection request: {}".format(request))

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)


def graas_ws_resource():
    # TODO: set url to something sane?
    factory = WebSocketServerFactory(u"ws://127.0.0.1:8080")
    factory.protocol = GraasServerWsProtocol
    return WebSocketResource(factory)
