from machine import Pin

from educore import pin
from pins_const import ports
import neopixel


class RGB:
    def __init__(self, ch=None, num=128, port=None):
        self.ch = ch
        if port is not None:
            if isinstance(port, list):
                s_pin = pin(port[0]).get_pin()
            else:
                s_pin = Pin(ports.get(str(port))[0])
        elif ch is not None:
            if isinstance(ch, pin):
                s_pin = ch.get_pin()
            else:
                s_pin = pin(ch).get_pin()
        else:
            s_pin = Pin(23)
        s_pin.init(Pin.OUT)

        self.num=num
        self.n = neopixel.NeoPixel(s_pin, num)

    def write(self, index, r, g, b):
        for i in index:
            self.n[i] = (r, g, b)
        self.n.write()

    def clear(self):
        for i in range(self.num):
            self.n[i]=(0,0,0)
        self.n.write()
