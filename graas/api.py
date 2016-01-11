""" GRaaS API. """

import pkg_resources

from klein import Klein

from twisted.python.filepath import FilePath
from twisted.web.static import File


class GraasApi(object):

    app = Klein()
    static_path = pkg_resources.resource_filename(__name__, "static")

    def __init__(self, gate_remote):
        self._gate_remote = gate_remote

    @app.route('/')
    def home(self, request):
        p = FilePath(self.static_path).child("index.html")
        return p.open().read()

    @app.route('/static/', branch=True)
    def static(self, request):
        return File(self.static_path)

    @app.route('/action/press', methods=['POST'])
    def action_press(self, request):
        if self._gate_remote is not None:
            self._gate_remote.press()
        return "Button pressed"
