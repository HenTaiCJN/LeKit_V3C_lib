from machine import Pin

from educore import pin
from pins_const import ports
import neopixel


class RGB:
    def __init__(self, ch=None, num=128, port=None):
        self.ch = ch
        self.is_borad = False
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
            self.is_borad = True
        s_pin.init(Pin.OUT)

        self.num = num
        self.n = neopixel.NeoPixel(s_pin, num)

    def write(self, index, r, g, b):
        if self.is_borad:
            for i in index:
                if i == 0:
                    self.n[2] = (r, g, b)
                if i == 2:
                    self.n[0] = (r, g, b)
        else:
            for i in index:
                self.n[i] = (r, g, b)
        self.n.write()

    def clear(self):
        for i in range(self.num):
            self.n[i] = (0, 0, 0)
        self.n.write()
