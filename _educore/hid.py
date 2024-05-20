from better_ble.application import HID as HHH


class HID:
    def __init__(self, name):
        self.ble = HHH(name=bytes(name, 'utf-8'), battery_level=100)

    def isconnected(self):
        return self.ble.isconnectde()

    def keyboard_send(self, code):
        if isinstance(code, list):
            if len(code) == 1:
                print('组合键至少有两个键')
            for i in range(len(code)):
                if code[i] == 0xE0 or code[i] == 0xE1 or code[i] == 0xE2:
                    self.ble.keyboard_press(code[i])
                    continue
                self.ble.keyboard_send(code[i])
            for i in range(len(code)):
                if code[i] == 0xE0 or code[i] == 0xE1 or code[i] == 0xE2:
                    self.ble.keyboard_release(code[i])
            return

        if isinstance(code, int):
            self.ble.keyboard_send(code)
            return
        for char in code:
            if char == " ":
                k_code = 0x2C
                self.ble.keyboard_send(k_code)
            elif ord("a") <= ord(char) <= ord("z"):
                k_code = 0x04 + ord(char) - ord("a")
                self.ble.keyboard_send(k_code)
            elif ord("A") <= ord(char) <= ord("Z"):
                self.ble.keyboard_press(0xE1)

                k_code = 0x04 + ord(char) - ord("A")
                self.ble.keyboard_send(k_code)

                self.ble.keyboard_release(0xE1)
            elif ord("0") <= ord(char) <= ord("9"):
                k_code = 0x1E + ord(char) - ord("0")
                self.ble.keyboard_send(k_code)
            else:
                continue

    def mouse_key(self, code):
        if code == 1:
            self.ble.mouse_click(1)
        if code == 2:
            self.ble.mouse_click(1)
            self.ble.mouse_click(1)

    def mouse_move(self, x, y, wheel=0):
        self.ble.mouse_move(x=x, y=y, wheel=wheel)
