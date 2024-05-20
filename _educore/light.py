from machine import Pin, ADC

from educore import pin
from pins_const import ports


class light:
    def __init__(self, ch=None, port=None):
        if port is not None:
            if isinstance(port, list):
                s_pin = pin(port[1]).get_pin()
            else:
                s_pin = Pin(ports.get(str(port))[1])
        elif ch is not None:
            if ch is None:
                s_pin = Pin(34)
            elif isinstance(ch, pin):
                s_pin = ch.get_pin()
            else:
                s_pin = pin(ch).get_pin()
        else:
            s_pin = Pin(34, mode=Pin.IN)

        s_pin.init(mode=Pin.IN)
        try:
            self.s_adc = ADC(s_pin)
        except:
            print('读取错误，请尝试使用AD口')
            return
        self.s_adc.width(ADC.WIDTH_12BIT)
        self.s_adc.atten(ADC.ATTN_11DB)

    def read(self):
        return self.s_adc.read()
