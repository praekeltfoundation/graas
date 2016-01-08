from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.trial.unittest import TestCase

from graas.hardware import AsyncIO
from graas.tests.helpers import TestGPIO

class TestAsyncIO(TestCase):
    def test_create_class(self):
        '''When the class is created, it should set the board mode to BOARD.'''
        io = AsyncIO(TestGPIO)
        self.assertEqual(TestGPIO._mode, TestGPIO.BOARD)

    @inlineCallbacks
    def test_setup_pin(self):
        '''setup_pin should setup the pin, and store the value in the pin
        state.'''
        io = AsyncIO(TestGPIO)
        yield io.setup_pin(0, TestGPIO.OUT, initial=TestGPIO.LOW)
        self.assertEqual(io.pin_state[0], {
            'mode': TestGPIO.OUT,
            'initial': TestGPIO.LOW,
        })
        self.assertEqual(TestGPIO._pins[0], {
            'direction': TestGPIO.OUT,
            'value': TestGPIO.LOW,
        })

    @inlineCallbacks
    def test_output_uninitialized(self):
        '''If the pin is not initialized, it should initialize it.'''
        io = AsyncIO(TestGPIO)
        yield io.output(0, TestGPIO.HIGH)
        self.assertEqual(io.pin_state[0], {
            'mode': TestGPIO.OUT,
            'initial': TestGPIO.HIGH,
        })
        self.assertEqual(TestGPIO._pins[0], {
            'direction': TestGPIO.OUT,
            'value': TestGPIO.HIGH,
        })

    @inlineCallbacks
    def test_output_initialized(self):
        '''If the pin is initialized, it should change the output.'''
        io = AsyncIO(TestGPIO)
        yield io.setup_pin(0, TestGPIO.OUT, initial=TestGPIO.LOW)
        yield io.output(0, TestGPIO.HIGH)
        self.assertEqual(io.pin_state[0], {
            'mode': TestGPIO.OUT,
            'initial': TestGPIO.LOW,
            'value': TestGPIO.HIGH,
        })
        self.assertEqual(TestGPIO._pins[0], {
            'direction': TestGPIO.OUT,
            'value': TestGPIO.HIGH,
        })

    @inlineCallbacks
    def test_input_uninitialized(self):
        '''Uninitialized input read should initialize the pin with a default
        pull down.'''
        io = AsyncIO(TestGPIO)
        result = yield io.input(0)
        self.assertEqual(result, TestGPIO.LOW)
        self.assertEqual(io.pin_state[0], {
            'mode': TestGPIO.IN,
            'pull_up_down': TestGPIO.PUD_DOWN,
        })
        self.assertEqual(TestGPIO._pins[0], {
            'direction': TestGPIO.IN,
            'pull': TestGPIO.PUD_DOWN,
        })

    @inlineCallbacks
    def test_input_initialized(self):
        '''Initialized input read should read the value of the pin.'''
        io = AsyncIO(TestGPIO)
        yield io.setup_pin(0, TestGPIO.IN, initial=TestGPIO.HIGH)
        result = yield io.input(0)
        self.assertEqual(result, TestGPIO.HIGH)
        self.assertEqual(TestGPIO._pins[0], {
            'direction': TestGPIO.IN,
            'value': TestGPIO.HIGH,
        })

    @inlineCallbacks
    def test_pulse(self):
        '''Pulse should pulse the the specified pin for the specified time.'''
        io = AsyncIO(TestGPIO)
        d = io.pulse(0, TestGPIO.HIGH, 0.01)
        self.assertEqual(TestGPIO._pins[0], {
            'direction': TestGPIO.OUT,
            'value': TestGPIO.HIGH,
        })
        yield d
        self.assertEqual(TestGPIO._pins[0], {
            'direction': TestGPIO.OUT,
            'value': TestGPIO.LOW,
        })


