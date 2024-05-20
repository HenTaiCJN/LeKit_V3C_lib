import time

import framebuf
from machine import SoftI2C, Pin

import GBfontget
import pins_const
from font import Font
from ssd1306 import SSD1306_I2C

res = []
punctuation_dit = {
    "。": b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x00\x24\x00\x24\x00\x18\x00\x00\x00\x00\x00',
    "￥": b'\x00\x00\x00\x00\x10\x10\x08\x20\x04\x40\x02\x80\x01\x00\x01\x00\x01\x00\x0f\xe0\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x00\x00',
    "、": b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x18\x00\x0c\x00\x04\x00\x00\x00\x00\x00'
}

class oled1306:
    def __init__(self, scl=pins_const.D10, sda=pins_const.D9):
        i2c = SoftI2C(scl=Pin(scl), sda=Pin(sda))
        addr = i2c.scan()

        if len(addr):
            self.oled = SSD1306_I2C(128, 64, i2c)
            self.FEN = Font(self.oled)
            self.FCN = GBfontget.gb2312(16)
            # oled.write_cmd(0xA0)
            # oled.write_cmd(0xC0)
            time.sleep_ms(300)
        else:
            print("连接128*64的OLED屏不成功")

    # 0代表只有英文1只有中文2代表混合,'判断字符串中英文状态'
    @staticmethod
    def contains_chinese_and_english(text):
        count = 0
        for char in text:
            if 0 <= ord(char) <= 127 and not '\u4e00' <= char <= '\uffff':
                pass
            elif '\u0000' <= char <= '\uffff' and not 0 <= ord(char) <= 127:
                count += 1
        if count == 0:
            return 0
        elif count == len(text):
            return 1
        else:
            return 2

    '显示纯中文'
    def chinese(self,ch_str, x_axis, y_axis, offset_=0):
        offset_ = offset_
        global res
        for k in ch_str:
            if k in punctuation_dit:
                fb = framebuf.FrameBuffer(bytearray(punctuation_dit[k]), 16, 16, framebuf.MONO_HLSB)
                self.oled.blit(fb, x_axis + offset_, y_axis)
                offset_ += 16
            else:
                t = self.FCN.str(k)
                byte_data = t.FONT[k]
                fb = framebuf.FrameBuffer(bytearray(byte_data), 16, 16, framebuf.MONO_HLSB)
                self.oled.blit(fb, x_axis + offset_, y_axis)
                offset_ += 16

    '混合显示'
    def displaytxt(self,string, x_axis, y_axis):
        offset = 0
        string = str(string)
        if self.contains_chinese_and_english(string) == 0:
            self.FEN.text(string, x_axis, y_axis, 16)
        elif self.contains_chinese_and_english(string) == 1:
            self.chinese(string, x_axis, y_axis)
        else:
            for char in string:
                if self.contains_chinese_and_english(char) == 0:
                    self.FEN.text(char, x_axis + offset, y_axis, 16)
                    offset += 8
                elif self.contains_chinese_and_english(char) == 1:
                    self.chinese(char, x_axis + offset, y_axis)
                    offset += 16

    '混合显示自动换行'

    def displaytxtauto(self,string, x_axis, y_axis):
        offsetx = x_axis
        offsety = y_axis
        lines = str(string).split("\n")
        for string in lines:
            for char in string:
                if self.contains_chinese_and_english(char) == 0:  # 0代表只有英文1只有中文2代表混合
                    if offsetx <= 128 - 8:
                        pass
                    else:
                        offsetx = 0
                        offsety += 16
                    self.FEN.text(char, offsetx, offsety, 16)
                    offsetx += 8
                elif self.contains_chinese_and_english(char) == 1:
                    if offsetx <= 128 - 16:
                        pass
                    else:
                        offsetx = 0
                        offsety += 16
                    self.chinese(char, offsetx - 16, offsety, 16)
                    offsetx += 16
            offsetx = 0
            offsety += 16
    def displayclear(self):
        self.oled.fill(0)

    def displayclearline(self,line):
        self.oled.fill_rect(0, line * 16, 128, 16, 0)

    def display_h_v_line(self,x, y, length, h_v, c=1):
        if h_v == 'h':
            self.oled.hline(x, y, length, c)
        else:
            self.oled.vline(x, y, length, c)

    def displayanyline(self,x1, y1, x2, y2, c=1):
        self.oled.line(x1, y1, x2, y2, c)

    def displayrect(self,x, y, w, h, c=1):
        self.oled.rect(x, y, w, h, c)

    def displayfill_rect(self,x, y, w, h, c=1):
        self.oled.fill_rect(x, y, w, h, c)

    def displaytxt_en(self,string: str, x_axis, y_axis, size=16):
        if self.contains_chinese_and_english(string) == 0:
            if size == 16 or size == 24 or size == 32:
                self.FEN.text(string, x_axis, y_axis, size)
            elif size == 8:
                self.oled.text(string, x_axis, y_axis, 1)
            else:
                print("font size must in 8,16,24,32")
    def displayshow(self):
        self.oled.show()
