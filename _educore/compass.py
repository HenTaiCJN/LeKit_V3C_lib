from machine import Pin, SoftI2C

from educore import pin
from qmc5883l_micropython import qmc5883l
from pins_const import ports


class qmc5883:
    def __init__(self, sda=None, scl=None, port=None):
        if sda is None and scl is None and port is None:
            print('暂不支持板载功能')
            return
        if port is not None:
            if isinstance(port, list):
                self.scl = pin(port[1]).get_pin()
                self.sda = pin(port[0]).get_pin()
            else:
                self.scl = Pin(ports.get(str(port))[0])
                self.sda = Pin(ports.get(str(port))[1])
        else:
            if isinstance(sda, pin):
                self.sda = sda.get_pin()
            else:
                self.sda = pin(sda).get_pin()

            if isinstance(scl, pin):
                self.scl = scl.get_pin()
            else:
                self.scl = pin(scl).get_pin()

        self.i2c = SoftI2C(sda=self.sda, scl=self.scl)
        self.qmc = qmc5883l.QMC5883L(self.i2c)

    def adjust(self):
        print('adjusting...')
        self.qmc.calibrate(5)
        print('adjust success')

    def direction(self):
        x, y, z, t = self.qmc.read_scaled()

        return self.qmc.get_angle(x, y)

    def getx(self):
        mag_x, mag_y, mag_z = self.qmc.read_raw()
        return mag_x

    def gety(self):
        mag_x, mag_y, mag_z = self.qmc.read_raw()
        return mag_y

    def getz(self):
        mag_x, mag_y, mag_z = self.qmc.read_raw()
        return mag_z
