import time

from machine import Pin

from adxl import adxl345
from educore import pin
from pins_const import ports


class accelerometer:
    def __init__(self, sda=None, scl=None, port=None):
        if port is not None:
            if isinstance(port, list):
                self.sda = pin(port[0]).get_pin()
                self.scl = pin(port[1]).get_pin()
            else:
                self.sda = Pin(ports.get(str(port))[1])
                self.scl = Pin(ports.get(str(port))[0])
        else:
            if isinstance(sda, pin):
                self.sda = sda.get_pin()
            else:
                self.sda = pin(sda).get_pin()

            if isinstance(scl, pin):
                self.scl = scl.get_pin()
            else:
                self.scl = pin(scl).get_pin()

        self.snsr = adxl345(self.scl, self.sda)

    @property
    def X(self):
        if self.snsr is not None:
            x, y, z = self.snsr.readXYZ()
            time.sleep(0.5)
            return x

    @property
    def Y(self):
        if self.snsr is not None:
            x, y, z = self.snsr.readXYZ()
            time.sleep(0.5)
            return y

    @property
    def Z(self):
        if self.snsr is not None:
            x, y, z = self.snsr.readXYZ()
            time.sleep(0.5)
            return z

    def shake(self):
        if self.snsr is not None:
            x1, y1, z1 = self.snsr.readXYZ()
            time.sleep(0.5)
            x2, y2, z2 = self.snsr.readXYZ()
            time.sleep(0.5)
            if abs(x1 - x2) > 20 or abs(y1 - y2) > 20 or abs(z1 - z2) > 20:
                return True
            else:
                return False
