""" GRaaS API. """

import pkg_resources

from klein import Klein

from twisted.python.filepath import FilePath
from twisted.web.static import File


class GraasApi(object):

    app = Klein()
    static_path = pkg_resources.resource_filename(__name__, "static")
    p = FilePath(static_path).child("index.html")

    def __init__(self, gate_remote):
        self._gate_remote = gate_remote

    def load_index_page(self):
        return self.p.open().read()

    @app.route('/')
    def home(self, request):
        return self.load_index_page()

    @app.route('/static/', branch=True)
    def static(self, request):
        return File(self.static_path)

    @app.route('/action/press', methods=['POST'])
    def action_press(self, request):
        if self._gate_remote is not None:git branch
            self._gate_remote.press()
        return self.load_index_page()
