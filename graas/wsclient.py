""" Utilities for connecting to q GRaaS server over a websocket and receiving
    requests to press the gate remote button.
    """

from autobahn.twisted.websocket import (
    WebSocketClientProtocol, WebSocketClientFactory)


class GraasClientWsProtocol(WebSocketClientProtocol):

    def onOpen(self):
        pass

    def onConnect(self, request):
        print("WebSocket connection request: {}".format(request))

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        pass


def graas_ws_client_factory():
    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = GraasClientWsProtocol
    return factory
