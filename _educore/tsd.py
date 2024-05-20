from machine import Pin

from educore import pin
from pins_const import ports

class TSD:
    def __init__(self, ch=None, port=None):
        if port is not None:
            if isinstance(port, list):
                self.s_pin = pin(port[0]).get_pin()
            else:
                self.s_pin = Pin(ports.get(str(port))[0])
        else:
            if isinstance(ch, pin):
                self.s_pin = ch.get_pin()
            else:
                self.s_pin = pin(ch).get_pin()
        self.s_pin.init(mode=Pin.IN)


    def read(self):
        return self.s_pin.value()