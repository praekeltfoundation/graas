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

    @app.route('/')
    def home(self, request):
        message = ''
        message_type = ''
        return HomePageElement(
            'Graas', message=message, message_type=message_type)

    @app.route('/static/', branch=True)
    def static(self, request):
        return File(self.static_path)

    @app.route('/action/press', methods=['POST'])
    def action_press(self, request):
        message = None
        message_type = None

        if self._gate_remote:
            pin = request.args.get('gatecode', [''])[0]
            if str(pin) == str(self._gate_remote._gate_remote_pin):
                self._gate_remote.press()
                message = 'Gate opened'
                message_type = 'info'
            else:
                message = 'Invalid pin'
                message_type = 'danger'

        return HomePageElement(
            'Graas', message=message, message_type=message_type)
