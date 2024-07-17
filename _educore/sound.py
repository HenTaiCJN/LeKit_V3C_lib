from machine import Pin, ADC

from educore import pin
from pins_const import ports


class sound:
    def __init__(self, ch=None, port=None):
        if ch is None and port is None:
            print('该传感器暂不支持板载功能')
            return
        if port is not None:
            if isinstance(port, list):
                self.s_pin = pin(port[0]).get_pin()
            else:
                self.s_pin = Pin(ports.get(str(port))[0])
        else:
            if isinstance(ch, pin):
                self.s_pin = ch.get_pin()
            else:
                self.s_pin = pin(ch).get_pin()
        self.s_pin.init(mode=Pin.IN)
        try:
            self.s_adc = ADC(self.s_pin)
        except:
            print('读取错误，请尝试使用AD口')
            return

    def read(self):
        return self.s_adc.read()
