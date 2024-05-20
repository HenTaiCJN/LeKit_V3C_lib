import math
import time

from machine import PWM, Pin

from educore import pin
from pins_const import ports


class servo:
    def __init__(self, ch=None, port=None, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self._angle = angle
        if port is not None:
            if isinstance(port, list):
                self.pwm = PWM(pin(port[0]).get_pin(), freq=freq)
            else:
                self.pwm = PWM(Pin(ports.get(str(port))[0]), freq=freq)
        else:
            if isinstance(ch, pin):
                self.pwm = PWM(ch.get_pin(), freq=freq)
            else:
                self.pwm = PWM(pin(ch).get_pin(), freq=freq)

    def write_us(self, us):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        if us == 0:
            self.pwm.duty(0)
            return
        us = min(self.max_us, max(self.min_us, us))
        duty = us * 1024 * self.freq // 1000000
        self.pwm.duty(duty)

    def angle(self, value=None, radians=None):
        """Move to the specified angle in ``degrees`` or ``radians``."""
        if value is None:
            value = math.degrees(radians)
        degrees = value % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self._angle
        self.write_us(us)