import time
from educore import  parrot, button


def sendfunction():
    M1.speed(100)
    time.sleep(12)
    M1.speed(0)
def sendfunction2():
    M1.speed(100)
    time.sleep(12)
    M1.speed(0)

M1 = parrot(in0=4, in1=5)
M1.speed(0)
btn = button(button.a)
btn2 = button(button.b)
btn.event_pressed = sendfunction
btn2.event_pressed = sendfunction2


M1.speed(-100)
