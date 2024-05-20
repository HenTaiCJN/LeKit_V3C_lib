import time

from machine import Pin, PWM

from educore import pin
from pins_const import *

from buzzconst import *
class speaker:
    def __init__(self, ch=None, port=None):
        if port is not None:
            if isinstance(port, list):
                self.s_pin = pin(port[0]).get_pin()
            else:
                self.s_pin = Pin(ports.get(str(port))[0])
        elif ch is not None:
            if isinstance(ch, pin):
                self.s_pin = ch.get_pin()
            else:
                self.s_pin = pin(ch).get_pin()
        elif port is None and ch is None:
            self.s_pin = Pin(19)

        self.s_pin.init(mode=Pin.OUT)
        self.pwm = PWM(self.s_pin)
        self.pwm.duty(0)

    def tone(self, freq, durl=150, duty=512):
        if type(freq) == list:
            freq = freq[0]
        self.pwm.duty(duty)
        if durl == 0 or durl is None:
            self.pwm.freq(freq)
        else:
            self.pwm.freq(freq)
            time.sleep(durl / 1000)
            self.pwm.duty(0)

    def stop(self):
        self.pwm.duty(0)