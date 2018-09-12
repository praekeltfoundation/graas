""" GRaaS API. """

import pkg_resources
from klein import Klein
from twisted.web.static import File

from .views import HomePageElement


class GraasApi(object):
    app = Klein()
    static_path = pkg_resources.resource_filename(__name__, "static")

    def __init__(self, gate_remote):
        self._gate_remote = gate_remote

    @app.route('/', methods=['POST', 'GET'])
    def home(self, request):
        message = ''
        message_type = ''
        pin = request.args.get('gatecode', [''])[0]

        if self._gate_remote and pin:
            if str(pin) == str(self._gate_remote._gate_remote_pin):
                self._gate_remote.press()
                message = 'Gate opened'
                message_type = 'info'
            else:
                message = 'Invalid pin'
                message_type = 'danger'

        return HomePageElement(
            'Graas', message=message, message_type=message_type)

    @app.route('/static/', branch=True)
    def static(self, request):
        return File(self.static_path)
