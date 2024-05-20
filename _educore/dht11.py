import dht
from machine import Pin

from educore import pin
from pins_const import ports


class dht11:
    def __init__(self, ch=None, port=None):

        if port is not None:
            if isinstance(port, list):
                self.s_pin = pin(port[1]).get_pin()
            else:
                self.s_pin = Pin(ports.get(str(port))[1])
        else:
            if isinstance(ch, pin):
                self.s_pin = ch.get_pin()
            else:
                self.s_pin = pin(ch).get_pin()

        self.s_pin.init(mode=Pin.IN, pull=Pin.PULL_UP)
        self.dht_sensor = dht.DHT22(self.s_pin)

    def read(self):
        self.dht_sensor.measure()
        temperature = self.dht_sensor.temperature()
        humidity = self.dht_sensor.humidity()
        data = (temperature, humidity)
        return data
