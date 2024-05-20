import gc
import json
from machine import Pin, PWM, ADC, UART, SoftI2C, unique_id
import time
# from LeKitV3action import *

from pins_const import *

chip_id = unique_id()
uuid = ':'.join(['{:02x}'.format(byte) for byte in chip_id])


class pin:
    pin_change = {0: D0, 1: D1, 2: D2, 3: D3, 4: D4, 5: D5, 6: D6, 7: D7, 8: D8, 9: D9, 10: D10, 11: D11, 12: D12,
                  13: D13, 14: D14, 15: D15,
                  'D0': D0, 'D1': D1, 'D2': D2, 'D3': D3, 'D4': D4, 'D5': D5, 'D6': D6, 'D7': D7, 'D8': D8, 'D9': D9,
                  'D10': D10, 'D11': D11,
                  'D12': D12, 'D13': D13, 'D14': D14, 'D15': D15, 'AD0': AD0, 'AD1': AD1, 'AD2': AD2
                  }

    def __init__(self, ch):
        ch = self.pin_change.get(ch, None)
        if ch is None:
            print('引脚错误，请确认引脚号')
        self.s_pin = Pin(ch)
        self.adc = None
        self.pwm = None
        PWM(self.s_pin).deinit()
        self._event_rising_callback = None
        self._event_falling_callback = None

    def get_pin(self):
        return self.s_pin

    @property
    def event_rising(self):
        return self._event_rising_callback

    @event_rising.setter
    def event_rising(self, callback):
        self._event_rising_callback = callback
        self.s_pin.irq(trigger=Pin.IRQ_RISING, handler=self.rising_callback)

    def rising_callback(self, p):
        if self._event_rising_callback is not None:
            self._event_rising_callback()

    @property
    def event_falling(self):
        return self._event_falling_callback

    @event_falling.setter
    def event_falling(self, callback):
        self._event_falling_callback = callback
        self.s_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.falling_callback)

    def falling_callback(self, p):
        if self._event_falling_callback is not None:
            self._event_falling_callback()
            gc.collect()

    def read_digital(self):
        self.s_pin.init(self.s_pin.IN, self.s_pin.PULL_DOWN)
        gc.collect()
        return self.s_pin.value()

    def read_analog(self):
        if self.pwm is not None:
            self.pwm.deinit()
            self.pwm = None
        if self.adc is None:
            self.s_pin.init(self.s_pin.IN, self.s_pin.PULL_DOWN)
            try:
                self.adc = ADC(self.s_pin)
            except:
                print('读取错误，请尝试使用AD口')
                return
        self.adc.width(ADC.WIDTH_12BIT)
        self.adc.atten(ADC.ATTN_11DB)
        gc.collect()
        return self.adc.read()

    def write_digital(self, value):
        self.s_pin.init(self.s_pin.OUT, self.s_pin.PULL_UP)
        self.s_pin.value(value)
        gc.collect()

    def write_analog(self, value, freq=5000):
        if self.pwm is None:
            self.s_pin.init(self.s_pin.OUT, self.s_pin.PULL_UP)
            self.pwm = PWM(self.s_pin, freq=freq)
        self.pwm.duty(value)
        gc.collect()


# oled
class _oled:

    def __init__(self):
        from ssd1306cn import oled1306
        self.oled = oled1306()

    def init(self, sda, scl):
        from ssd1306cn import oled1306
        self.oled = oled1306(sda=sda, scl=scl)

    def print(self, txt):
        self.oled.displayclear()
        self.oled.displaytxtauto(txt, 0, 0)
        self.oled.displayshow()
        gc.collect()

    def clear(self):
        self.oled.displayclear()
        self.oled.displayshow()


oled = _oled()


class speaker:

    def __init__(self, ch=None, port=None):
        from _educore.speaker import speaker as sp
        self.s = sp(ch=ch, port=port)

    def tone(self, freq, dual=None, durl=None):
        if dual is None:
            dual = durl
        self.s.tone(freq=freq, durl=dual)
        gc.collect()

    def stop(self):
        self.s.stop()
        gc.collect()


# 电机控制
class parrot:
    M1 = 1
    M2 = 2

    def __init__(self, ch=None, in0=None, in1=None):
        from _educore.parrot import parrot as pr
        self.p = pr(ch=ch, in0=in0, in1=in1)

    def speed(self, speed=None):
        self.p.set_speed(speed)
        gc.collect()


# 舵机控制
class servo:

    def __init__(self, ch=None, port=None):
        from _educore.servo import servo as sv
        time.sleep(1)
        self.s = sv(ch=ch, port=port)

    def angle(self, value=None, radians=None):
        self.s.angle(value, radians)


# RGB
class rgb:
    def __init__(self, ch=None, num=3, port=None):
        from _educore.rgb import RGB
        self.rgb = RGB(ch=ch, num=num, port=port)
        gc.collect()

    def write(self, index, r, g, b):
        self.rgb.write(index, r, g, b)
        gc.collect()

    def clear(self):
        self.rgb.clear()
        gc.collect()


# 读取声音
class sound:

    def __init__(self, ch=None, port=None):
        from _educore.sound import sound as sd
        self.s = sd(ch=ch, port=port)

    def read(self):
        return self.s.read()


# 读取光线
class light:
    def __init__(self, ch=None, port=None):
        from _educore.light import light as lg
        self.s = lg(ch=ch, port=port)

    def read(self):
        return self.s.read()


# 板载按键
class button:
    a = '18'
    b = '5'

    def __init__(self, ch=None, port=None):
        from _educore.button import button as btn
        self.btn = btn(ch=ch, port=port)

    def status(self):
        return self.btn.status()

    @property
    def event_pressed(self):
        return self.btn.event_pressed

    @event_pressed.setter
    def event_pressed(self, callback):
        self.btn.event_pressed = callback


# 加速度传感器
class accelerometer:

    def __init__(self, sda=None, scl=None, port=None):
        from _educore.accelerometer import accelerometer as acc
        self.acc = acc(sda=sda, scl=scl, port=port)

    def X(self):
        gc.collect()
        return self.acc.X

    def Y(self):
        gc.collect()
        return self.acc.Y

    def Z(self):
        gc.collect()
        return self.acc.Z

    def shake(self):
        gc.collect()
        return self.acc.shake()


# dht11温湿度
class dht11:

    def __init__(self, ch=None, port=None):
        from _educore.dht11 import dht11 as dt
        self.dht = dt(ch=ch, port=port)

    def read(self):
        return self.dht.read()


# DS18b20温度传感器
class ds18b20:

    def __init__(self, ch=None, port=None):
        from _educore.ds18b20 import ds18b20 as ds
        self.ds = ds(ch=ch, port=port)

    def read(self):
        return self.ds.read()


# 超声波测距
class ultrasonic:

    def __init__(self, trig=None, echo=None, port=None):
        from _educore.ultrasonic import Ultrasonic
        self.u = Ultrasonic(trig=trig, echo=echo, port=port)

    def distance(self):
        return self.u.distance()

    def distance_mm(self):
        return self.u.distance_mm()


class rfid:
    def __init__(self, sda=None, scl=None, port=None, address=None):
        from _educore.rfid import Scan_Rfid
        self.rfid = Scan_Rfid(sda=sda, scl=scl, port=port, address=address)

    def scanning(self, wait=True):
        return self.rfid.scanning(wait=wait)


class tsd:

    def __init__(self, ch=None, port=None):
        from _educore.tsd import TSD
        self.tsd = TSD(ch=ch, port=port)

    def read(self):
        gc.collect()
        return self.tsd.read()


class pressure:

    def __init__(self, sda=None, scl=None, port=None):
        from _educore.pressure import pressure as ps
        self.ps = ps(sda=sda, scl=scl, port=port)

    def read(self):
        gc.collect()
        return self.ps.read()


class compass:

    def __init__(self, sda=None, scl=None, port=None):
        from _educore.compass import qmc5883 as qmc
        self.qmc = qmc(sda=sda, scl=scl, port=port)

    def adjust(self):
        self.qmc.adjust()
        gc.collect()

    def direction(self):
        gc.collect()
        return self.qmc.direction()

    def getx(self):
        return self.qmc.getx()

    def gety(self):
        return self.qmc.gety()

    def getz(self):
        return self.qmc.getz()


# 蓝牙HID设备模块
class Keyboard:
    CLICK = 1
    DCLICK = 2
    SPACE = 0x2C
    ENTER = 0x28
    CTRL = 0xE0
    SHIFT = 0xE1
    ALT = 0xE2
    LEFT = 0x50
    RIGHT = 0x4F
    DOWN = 0x51
    UP = 0x52
    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    _8 = '8'
    _9 = '0'

    def __getattr__(self, letter):
        return letter


keycode = Keyboard()


class hid:
    def __init__(self, name):
        from _educore.hid import HID
        self.ble = HID(name)
        gc.collect()

    def isconnected(self):
        return self.ble.isconnected()

    def keyboard_send(self, code):
        self.ble.keyboard_send(code)
        gc.collect()

    def mouse_key(self, code):
        self.ble.mouse_key(code)
        gc.collect()

    def mouse_move(self, x, y, wheel=0):
        self.ble.mouse_move(x=x, y=y, wheel=wheel)


# 连接wifi

class wifi:
    import wificonnect as wc
    def __init__(self):
        pass

    @classmethod
    def connect(cls, ssid, psd, timeout=10000):
        cls.wc.start()
        cls.wc.connect(ssid, psd, timeout)
        gc.collect()

    @classmethod
    def close(cls):
        cls.wc.close()
        gc.collect()

    @classmethod
    def status(cls):
        cls.wc.status()

    @classmethod
    def info(cls):
        cls.wc.info()


# MQTT
class mqttclient:
    from _educore.mqtt import MQTTClient
    def __init__(self):
        pass

    @classmethod
    def connect(cls, server, port, client_id='', user='', psd=''):
        cls.MQTTClient.connect(server=server, port=port, client_id=client_id, user=user, psd=psd)

    @classmethod
    def connected(cls):
        return cls.MQTTClient.connected()

    @classmethod
    def publish(cls, topic, content):
        cls.MQTTClient.publish(topic=topic, content=content)

    @classmethod
    def message(cls, topic):
        return cls.MQTTClient.receive(topic=topic)

    @classmethod
    def received(cls, topic, callback):
        cls.MQTTClient.Received(topic=topic, callback=callback)


class webcamera:
    from _educore.webcamera import webcamera

    @classmethod
    def connect(cls, id):
        cls.webcamera.connect(id)

    @classmethod
    def result(cls):
        return cls.webcamera.result()


def get_dict_from_file(filename):
    # 打开文件并读取所有行
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 初始化空字典
    dic = {}

    # 遍历每一行并生成键值对
    for line in lines:
        # 去除行末尾的换行符
        line = line.rstrip('\n')

        # 将行内容拆分为键和值
        key, value = line.split(' ', 1)

        # 如果键已经存在于字典中，则忽略该行
        if key in dic:
            continue

        # 将键值对添加到字典中
        dic[key] = value

    # 返回生成的字典
    gc.collect()
    return dic


def get_dict_from_str(s):
    result_dict = {}

    # 使用分号或换行符分割字符串
    entries = s.replace('\n', ';').split(';')

    for entry in entries:
        # 移除可能存在的多余空格
        entry = entry.strip()

        # 使用空格分割键值对
        key_value = entry.split(None, 1)

        # 确保有两个元素，否则跳过当前条目
        if len(key_value) == 2:
            key, value = key_value
            result_dict[key] = value

    gc.collect()
    return result_dict


class led:
    def __init__(self, ch=None, port=None):
        if port is not None:
            if isinstance(port, list):
                self.led_pin = pin(port[0]).get_pin()
            else:
                self.led_pin = Pin(ports.get(str(port))[0])
        else:
            if isinstance(ch, pin):
                self.led_pin = ch.get_pin()
            else:
                self.led_pin = pin(ch).get_pin()

        self.led_pin.init(mode=Pin.OUT, pull=-1)
        self.led_pin.value(0)

    def on(self):
        self.led_pin.value(1)
        gc.collect()

    def off(self):
        self.led_pin.value(0)
        gc.collect()


class singlebutton:
    def __init__(self, ch=None, port=None):
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

        self.s_pin.init(mode=Pin.IN, pull=-1)

    def read(self):
        gc.collect()
        return self.s_pin.value()


class fourfoldbut:
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

        self.s_pin.init(mode=Pin.IN, pull=-1)
        self.adc_sig = ADC(self.s_pin)
        self.adc_sig.width(ADC.WIDTH_12BIT)
        self.adc_sig.atten(ADC.ATTN_11DB)

    def read(self):
        gc.collect()
        return self.adc_sig.read()

    def button(self):
        if self.read() == 0:
            return 'A'
        elif 800 < self.read() < 1500:
            return 'B'
        elif 1800 < self.read() < 2500:
            return 'C'
        elif 3000 < self.read() < 4095:
            return 'D'
        else:
            return None


class IR:
    CODE = {
        162: "ch-", 98: "ch", 226: "ch+",
        34: "prev", 2: "next", 194: "play/stop",
        152: "0", 104: "*", 176: "#",
        224: "-", 168: "+", 144: "EQ",
        104: "0", 152: "100+", 176: "200+",
        48: "1", 24: "2", 122: "3",
        16: "4", 56: "5", 90: "6",
        66: "7", 74: "8", 82: "9"
    }

    def __init__(self, ch=None, port=None):
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
        self.s_pin.init(Pin.IN, Pin.PULL_UP)

        self.irRecv = self.s_pin
        self.irRecv.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.__handler)  # 配置中断信息
        self.ir_step = 0
        self.ir_count = 0
        self.buf64 = [0 for i in range(64)]
        self.recived_ok = False
        self.cmd = None
        self.cmd_last = None
        self.repeat = 0
        self.repeat_last = None
        self.t_ok = None
        self.t_ok_last = None
        self.start = 0
        self.start_last = 0
        self.changed = False
        self.actions = {'ir': []}

    def __handler(self, source):
        """
        中断回调函数
        """
        thisComeInTime = time.ticks_us()

        # 更新时间
        curtime = time.ticks_diff(thisComeInTime, self.start)
        self.start = thisComeInTime

        if 8500 <= curtime <= 9500:
            self.ir_step = 1
            return

        if self.ir_step == 1:
            if 4000 <= curtime <= 5000:
                self.ir_step = 2
                self.recived_ok = False
                self.ir_count = 0
                self.repeat = 0
            elif 2000 <= curtime <= 3000:  # 长按重复接收
                self.ir_step = 3
                self.repeat += 1

        elif self.ir_step == 2:  # 接收4个字节
            self.buf64[self.ir_count] = curtime
            self.ir_count += 1
            if self.ir_count >= 64:
                self.recived_ok = True
                self.t_ok = self.start  # 记录最后ok的时间
                self.ir_step = 0
                self.__check_cmd()

        elif self.ir_step == 3:  # 重复
            if 500 <= curtime <= 650:
                self.repeat += 1

    def __check_cmd(self):
        byte4 = 0
        for i in range(32):
            x = i * 2
            t = self.buf64[x] + self.buf64[x + 1]
            byte4 <<= 1
            if 1800 <= t <= 2800:
                byte4 += 1
        user_code_hi = (byte4 & 0xff000000) >> 24
        user_code_lo = (byte4 & 0x00ff0000) >> 16
        data_code = (byte4 & 0x0000ff00) >> 8
        data_code_r = byte4 & 0x000000ff
        self.cmd = data_code
        if not self.actions['ir'] == []:
            try:
                self.actions['ir'][0]()
            except ZeroDivisionError:
                print("function error")

    def scan(self):
        # 接收到数据
        if self.recived_ok:
            self.__check_cmd()
            self.recived_ok = False

        # 数据有变化
        if self.cmd != self.cmd_last or self.repeat != self.repeat_last or self.t_ok != self.t_ok_last:
            self.changed = True
        else:
            self.changed = False

        # 更新
        self.cmd_last = self.cmd
        self.repeat_last = self.repeat
        self.t_ok_last = self.t_ok
        # 对应按钮字符
        s = self.CODE.get(self.cmd)
        return self.changed, s, self.repeat, self.t_ok

    def setcb(self, function):
        try:
            self.actions['ir'] = [function]
            return True
        except:
            print("un-existed function")

    def read(self):
        gc.collect()
        return self.cmd


class apds:
    def __init__(self, sda=None, scl=None, port=None):
        from apds9960 import uAPDS9960 as APDS9960
        from apds9960 import const
        if port is not None:
            if isinstance(port, list):
                self.sda = pin(port[0]).get_pin()
                self.scl = pin(port[1]).get_pin()
            else:
                self.sda = Pin(ports.get(str(port))[1])
                self.scl = Pin(ports.get(str(port))[0])
        else:
            if isinstance(sda, pin):
                self.sda = sda.get_pin()
            else:
                self.sda = pin(sda).get_pin()

            if isinstance(scl, pin):
                self.scl = scl.get_pin()
            else:
                self.scl = pin(scl).get_pin()

        self.bus = SoftI2C(sda=self.sda, scl=self.scl)
        self.apds = APDS9960(self.bus)
        self.dirs = {
            const.APDS9960_DIR_NONE: "none",
            const.APDS9960_DIR_LEFT: "left",
            const.APDS9960_DIR_RIGHT: "right",
            const.APDS9960_DIR_UP: "up",
            const.APDS9960_DIR_DOWN: "down",
            const.APDS9960_DIR_NEAR: "near",
            const.APDS9960_DIR_FAR: "far",
        }
        self.apds.setProximityIntLowThreshold(50)
        self.apds.enableGestureSensor()
        self.apds.enableProximitySensor()
        self.apds.enableLightSensor()
        self.res = ""

    def read(self):
        try:
            flag = self.apds.isGestureAvailable()
        except:
            return None
        if flag:
            try:
                motion = self.apds.readGesture()
                self.res = self.dirs.get(motion, "unknown")
                #             print("Gesture={}".format(self.dirs.get(motion, "unknown")))
                return self.res
            except:
                return None
        else:
            return None

    def readProximity(self):
        gc.collect()
        return self.apds.readProximity()

    def readLight(self):
        gc.collect()
        return self.apds.readAmbientLight()


class linefinder:
    def __init__(self, s1=None, s2=None, port=None):
        if port is not None:
            if isinstance(port, list):
                self.s1_pin = pin(port[1]).get_pin()
                self.s2_pin = pin(port[0]).get_pin()
            else:
                self.s1_pin = Pin(ports.get(str(port))[1])
                self.s2_pin = Pin(ports.get(str(port))[0])
        else:
            if isinstance(s1, pin):
                self.s1_pin = s1.get_pin()
            else:
                self.s1_pin = pin(s1).get_pin()

            if isinstance(s2, pin):
                self.s2_pin = s2.get_pin()
            else:
                self.s2_pin = pin(s2).get_pin()

        self.s1_pin.init(mode=Pin.IN, pull=-1)
        self.s2_pin.init(mode=Pin.IN, pull=-1)

    def reads1(self):
        gc.collect()
        return self.s1_pin.value()

    def reads2(self):
        gc.collect()
        return self.s2_pin.value()


class ps2but(object):
    pin_change = {0: D0, 1: D1, 2: D2, 3: D3, 4: D4, 5: D5, 6: D6, 7: D7, 8: D8, 9: D9, 10: D10, 11: D11, 12: D12,
                  13: D13, 14: D14, 15: D15,
                  'D0': D0, 'D1': D1, 'D2': D2, 'D3': D3, 'D4': D4, 'D5': D5, 'D6': D6, 'D7': D7, 'D8': D8, 'D9': D9,
                  'D10': D10, 'D11': D11,
                  'D12': D12, 'D13': D13, 'D14': D14, 'D15': D15, 'AD0': AD0, 'AD1': AD1, 'AD2': AD2
                  }

    def __init__(self, tx=None, rx=None, port=None):
        if port is not None:
            if isinstance(port, list):
                self.tx = self.pin_change.get(port[0])
                self.rx = self.pin_change.get(port[1])
            else:
                self.tx = ports.get(str(port))[0]
                self.rx = ports.get(str(port))[1]
        else:
            if isinstance(tx, pin):
                print('请直接输入引脚号')
            else:
                self.tx = self.pin_change.get(tx)

            if isinstance(rx, pin):
                print('请直接输入引脚号')
            else:
                self.rx = self.pin_change.get(rx)

        self.uart = UART(1, baudrate=9600, rx=self.rx, tx=self.tx)
        self.data = {'X': None, 'Y': None, 'Button': None}

    def read(self):
        self.msg = ""
        self.data = {'X': None, 'Y': None, 'Button': None}
        self.uart.write('readdown')
        time.sleep(1 / 10)
        if self.uart.any():
            self.msg = self.uart.readline().decode()
        if self.msg == "":
            return
        try:
            self.data = json.loads(self.msg)
        except Exception as e:
            pass

    def getX(self):
        self.read()
        gc.collect()
        return self.data['X']

    def getY(self):
        self.read()
        gc.collect()
        return self.data['Y']

    def getBt(self):
        self.read()
        gc.collect()
        return self.data['Button']


class dig_display:
    def __init__(self, dio=None, clk=None, port=None):
        from tm1637 import TM1637
        if port is not None:
            if isinstance(port, list):
                self.dio = pin(port[0]).get_pin()
                self.clk = pin(port[1]).get_pin()
            else:
                self.dio = Pin(ports.get(str(port))[0])
                self.clk = Pin(ports.get(str(port))[1])
        else:
            if isinstance(dio, pin):
                self.dio = dio.get_pin()
            else:
                self.dio = pin(dio).get_pin()

            if isinstance(clk, pin):
                self.clk = clk.get_pin()
            else:
                self.clk = pin(clk).get_pin()

        self.smg = TM1637(clk=self.clk, dio=self.dio)

    def show(self, string):
        self.smg.show(str(string))
        gc.collect()

    def showscroll(self, string):
        self.smg.scroll(str(string))
        gc.collect()
