import time

from machine import Pin, ADC

from educore import pin


class sound:
    def __init__(self, ch=None, port=None):
        if ch is None and port is None:
            self.s_pin = Pin(35)
        elif port is not None:
            print('不支持端口')
            return
        else:
            if isinstance(ch, pin):
                self.s_pin = ch.get_pin()
            else:
                self.s_pin = pin(ch).get_pin()

        self.s_pin.init(mode=Pin.IN)

        try:
            self.s_adc = ADC(self.s_pin)
        except:
            print('读取错误，请尝试使用0号口或1号口')
            return
        self.s_adc.width(ADC.WIDTH_12BIT)
        self.s_adc.atten(ADC.ATTN_11DB)

    def read(self):
        return self.s_adc.read()

a=sound(15)
while 1:
    print(a.read())
    time.sleep(1)