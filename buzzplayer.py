from machine import Pin
from machine import PWM
from time import sleep_ms
from pins_const import *
class BUZZER(object):
    def __init__(self):
        self.pwm = PWM(Pin(19, Pin.OUT))
        self.pwm.duty(0)
    def play(self, melodies, delay=150, duty=512):
        for note in melodies:
            if note:
                self.pwm.freq(note)
            self.pwm.duty(duty)
            sleep_ms(delay)
        self.pwm.duty(0)