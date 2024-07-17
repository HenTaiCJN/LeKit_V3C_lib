import time

import gc
from machine import Timer

from _educore.ble import CBle
from educore import button

bleCode: None | CBle
bleCode = CBle("LekitV3C")
bleCode.start_advertising()
flag = False


def ignore():
    pass


def sendfunction():
    global bleCode, flag
    while btn.status():
        if btnb.status():
            bleCode.showCode()
            btn.event_pressed = ignore
            flag = True
            break
        time.sleep_ms(100)


def close(_):
    if bleCode is not None and not flag:
        if bleCode.status:
            bleCode.close()
            btn.event_pressed = ignore
            gc.collect()


btn = button(button.a)
btnb = button(button.b)

btn.event_pressed = sendfunction
# Timer(0).init(period=5000, mode=Timer.ONE_SHOT, callback=close)
