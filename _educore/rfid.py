import time

from machine import Pin, I2C

import rc522i2c as RFIDI2CMicroPython
from educore import pin
from pins_const import ports


class RF:
    def __init__(self, uid):
        self.uid = uid

    def serial_number(self):
        if self.uid is None:
            return None
        return f"{self.uid[0]}-{self.uid[1]}-{self.uid[2]}-{self.uid[3]}"


class Scan_Rfid:
    def __init__(self, sda=None, scl=None, port=None, address=None):
        if port is not None:
            if isinstance(port, list):
                self.sda = pin(port[0]).get_pin()
                self.scl = pin(port[1]).get_pin()
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

        self.i2c = I2C(1, scl=self.scl, sda=self.sda, freq=100000)
        if address is not None:
            self.MRFC522Reader = RFIDI2CMicroPython.MRFC522(self.i2c, address)
        else:
            self.MRFC522Reader = RFIDI2CMicroPython.MRFC522(self.i2c)

        self.MRFC522Reader.showReaderDetails()

    def scanning(self, wait=True):
        now = None
        if isinstance(wait, bool):
            wait_time = None
        elif isinstance(wait, int):
            wait_time = wait
            now = time.time()
        else:
            print('请输入True或者等待多少秒（整数）')
            return

        while True:
            # 超时判断
            if wait_time is not None:
                if time.time() > now + wait_time:
                    return RF(None)

            try:
                (status, backData, tagType) = self.MRFC522Reader.scan()
                if status == self.MRFC522Reader.MI_OK:
                    (status, uid, backBits) = self.MRFC522Reader.transceive()
                    if status == self.MRFC522Reader.MI_OK:
                        return RF(uid)
                continue
            except Exception as e:
                if len(self.i2c.scan()) != 0:
                    try:
                        self.MRFC522Reader = RFIDI2CMicroPython.MRFC522(self.i2c)
                        continue
                    except  Exception as e:
                        pass
            finally:
                time.sleep(0.5)