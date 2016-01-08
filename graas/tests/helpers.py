class GPIOException(Exception):
    pass


class TestGPIO(object):
    '''An in-memory implementation of the GPIO module for the Raspberry Pi.'''
    BOARD = 'board'
    BCM = 'bcm'
    IN = 'in'
    OUT = 'out'
    HIGH = True
    LOW = False
    PUD_UP = HIGH
    PUD_DOWN = LOW

    _mode = None
    _pins = {}

    @classmethod
    def setmode(cls, mode):
        cls._mode = mode

    @classmethod
    def setup(cls, channel, direction, initial=None, pull_up_down=None):
        cls._pins[channel] = {
            'direction': direction,
        }
        if initial is not None:
            cls.output(channel, initial)
        if pull_up_down is not None:
            cls._pins[channel]['pull'] = pull_up_down

    @classmethod
    def output(cls, channel, value):
        if cls._pins.get(channel) is None:
            raise GPIOException('Channel %r has not been setup' % channel)
        if value:
            cls._pins[channel]['value'] = cls.HIGH
        else:
            cls._pins[channel]['value'] = cls.LOW

    @classmethod
    def input(cls, channel):
        channel = cls._pins.get(channel)
        if channel is None:
            raise GPIOException('Channel %r has not been setup' % channel)
        if channel['direction'] == cls.IN and channel.get('value') is None:
            return channel.get('pull')
        return channel.get('value')
