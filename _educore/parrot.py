from machine import Pin, PWM

from educore import pin
from pins_const import ports


class parrot:
    M1 = 1
    M2 = 2
    M3 = 3
    M4 = 4

    def __init__(self, ch=None, in0=None, in1=None):
        self.ch = ch
        self.in0 = in0
        self.in1 = in1
        self.is_onboard = False

        self.motor_pin1 = None
        self.motor_pin2 = None
        self.motor_pwm = None
        self.speed = None

        if self.in0 is None or self.in1 is None:
            self.init_onboard_motor()
        else:
            self.init_external_motor()

    def init_onboard_motor(self):
        ch_sel = ports
        self.motor_pin1 = Pin(ch_sel[f'{self.ch}'][0], mode=Pin.OUT, pull=Pin.PULL_UP)
        self.motor_pin2 = Pin(ch_sel[f'{self.ch}'][1], mode=Pin.OUT, pull=Pin.PULL_UP)
        self.motor_pwm = PWM(self.motor_pin2)

    def init_external_motor(self):
        if isinstance(self.in0, int):
            self.motor_pin1 = pin(self.in0).get_pin()
        else:
            self.motor_pin1 = self.in0.get_pin()

        if isinstance(self.in1, int):
            self.motor_pin2 = pin(self.in1).get_pin()
        else:
            self.motor_pin2 = self.in1.get_pin()

        self.motor_pin1.init(mode=Pin.OUT, pull=Pin.PULL_UP)
        self.motor_pin2.init(mode=Pin.OUT, pull=Pin.PULL_UP)
        self.motor_pwm = PWM(self.motor_pin2)

    def set_speed(self, speed=None):

        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100

        self.speed = speed
        self.updata_onboard()

    def updata_onboard(self):
        self.motor_pwm.deinit()
        self.motor_pwm = PWM(self.motor_pin2, freq=5000)
        if self.speed > 0:
            self.motor_pin1.value(1)
            self.motor_pwm.duty(int((100 - self.speed) * 10.23))
        elif self.speed < 0:
            self.motor_pin1.value(0)
            self.motor_pwm.duty(int(-self.speed * 10.23))
        else:
            self.motor_pin1.value(0)
            self.motor_pwm.duty(0)
