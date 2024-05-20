from machine import Pin

from educore import pin
from pins_const import ports

class button:
    def __init__(self,ch=None,port=None):
        self._event_pressed =None

        if port is not None:
            if isinstance(port, list):
                self.s_pin = pin(port[0]).get_pin()
            else:
                self.s_pin = Pin(ports.get(str(port))[0])
        else:
            if isinstance(ch, pin):
                self.s_pin = ch.get_pin()
            elif isinstance(ch, str):
                self.s_pin=Pin(int(ch))
            else:
                self.s_pin = pin(ch).get_pin()

    def status(self):
        return self.s_pin.value()

    @property
    def event_pressed(self):
        return self._event_pressed
    @event_pressed.setter
    def event_pressed(self, callback):
        self._event_pressed=callback
        self.s_pin.irq(trigger=Pin.IRQ_RISING, handler=self.callback)
    def callback(self,e):
        if self._event_pressed is not None:
            self._event_pressed()
