from twisted.internet import task, reactor
from twisted.internet.defer import succeed, inlineCallbacks, returnValue


class AsyncIO(object):

    def __init__(self, GPIO):
        '''
        GPIO - Raspberry Pi GPIO module to control hardware
        '''
        GPIO.setmode(GPIO.BOARD)
        self.pin_state = {}

        self.INPUT = GPIO.IN
        self.OUTPUT = GPIO.OUT
        self.HIGH = GPIO.HIGH
        self.LOW = GPIO.LOW
        self.PULL_UP = GPIO.PUD_UP
        self.PULL_DOWN = GPIO.PUD_DOWN

        self.GPIO = GPIO

    def setup_pin(self, pin, mode, **kwargs):
        '''
        Initialize a pin.

        :param int pin: The number of the pin to set.
        :param mode: The mode to set the pin. Either INPUT or OUTPUT.
        :param initial:
            The initial value for the pin. Either LOW or HIGH. Defaults to LOW.
        '''
        self.GPIO.setup(pin, mode, **kwargs)
        self.pin_state[pin] = kwargs
        self.pin_state[pin]['mode'] = mode
        return succeed(None)

    def output(self, pin, value):
        '''
        Set the output of a pin. Initializes the pin if required.

        :param int pin: The number of the pin to set
        :param value: Either LOW or HIGH
        '''
        if (pin in self.pin_state and
                self.pin_state[pin]['mode'] == self.OUTPUT):
            self.GPIO.output(pin, value)
            self.pin_state[pin]['value'] = value
            return succeed(None)
        return self.setup_pin(pin, self.OUTPUT, initial=value)

    @inlineCallbacks
    def input(self, pin, pull=None):
        '''
        Gets the value of a pin. Initializes the pin if required.

        :param int pin: The pin to read.
        :param pull:
            Whether to pull the pin up or down. Either PULL_UP or PULL_DOWN.
            Defaults to PULL_DOWN

        Returns a deferred which fires with either HIGH or LOW.
        '''
        if pull is None:
            pull = self.PULL_DOWN
        if not (
                pin in self.pin_state and
                self.pin_state[pin]['mode'] == self.INPUT):
            yield self.setup_pin(pin, self.INPUT, pull_up_down=pull)
        returnValue(self.GPIO.input(pin))

    @inlineCallbacks
    def pulse(self, pin, value, duration):
        '''
        Pulses the pin. If value is high, sets the pin to high for duration
        before setting it to low. If low, sets the pin to low for duration
        before setting it to high.

        :param int pin: The number of the pin to pulse.
        :param value: The value to pulse. Either HIGH or LOW.
        :param float duration: The duration to pulse for.

        Returns a deferred that fires when the pulse has completed.
        '''
        yield self.output(pin, value)
        yield task.deferLater(reactor, duration, self.output, pin, not value)
        returnValue(None)


class IGateRemote(object):
    """ Interface to a GateRemote. """

    def ws_resource(self):
        """ Return a web socket resource for clients to connect to (or None).
        """

    def press(self):
        """ Press the gate remote and return a deferred that fires when done.
        """


class GateRemote(object):
    def __init__(self, pin, _gpio=None):
        if _gpio is None:
            import RPi.GPIO as _gpio
        self._asyncio = AsyncIO(_gpio)
        self._gate_remote_pin = pin

    def ws_resource(self):
        None

    def press(self):
        return self._asyncio.pulse(
            self._gate_remote_pin, self._asyncio.HIGH, 0.5)


class SimulatedGateRemote(GateRemote):
    def __init__(self, pin):
        from graas.tests.helpers import TestGPIO as _gpio
        super(SimulatedGateRemote, self).__init__(pin, _gpio=_gpio)


class ProxiedGateRemote(object):
    def __init__(self):
        from .wsproxy import graas_ws_resource
        self._resource = graas_ws_resource()

    def ws_resource(self):
        return self._resource

    def press(self):
        print "Pressed"
