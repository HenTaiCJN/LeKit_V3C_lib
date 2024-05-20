import time

from machine import Pin, time_pulse_us

from educore import pin
from pins_const import ports


class Ultrasonic:
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trig=None, echo=None, port=None, echo_timeout_us=500 * 2 * 30):
        self.echo_timeout_us = echo_timeout_us
        if port is not None:
            if isinstance(port, list):
                self.trigger = pin(port[0]).get_pin()
                self.echo = pin(port[1]).get_pin()
            else:
                self.trigger = Pin(ports.get(str(port))[1])
                self.echo = Pin(ports.get(str(port))[0])
        else:
            if isinstance(trig, pin):
                self.trigger = trig.get_pin()
            else:
                self.trigger = pin(trig).get_pin()

            if isinstance(echo, pin):
                self.echo = echo.get_pin()
            else:
                self.echo = pin(echo).get_pin()

        self.trigger.init(mode=Pin.OUT, pull=-1)
        self.trigger.value(0)
        self.echo.init(mode=Pin.IN, pull=-1)
        # Init echo pin (in)

        self.__limit = 400  # cm

    def _send_pulse_and_wait(self):
        self.trigger.value(0)  # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)
        pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
        return pulse_time

    def distance(self):
        pulse_time = self._send_pulse_and_wait()
        if pulse_time != (-1 or -2):
            cms = (pulse_time / 2) / 29.1
            return cms
        else:
            return int(self.__limit)

    def distance_mm(self):
        pulse_time = self._send_pulse_and_wait()
        if pulse_time != (-1 or -2):
            mm = pulse_time * 100 // 582
            return mm
        else:
            return self.__limit * 10