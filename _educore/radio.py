import json
import network
import espnow


class Radio:
    def __init__(self, code):
        network.WLAN(network.STA_IF).active(True)

        self.func = None
        self.code = code
        self.msg = None
        # 初始化ESP-NOW
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)

        self.e = espnow.ESPNow()
        self.e.active(True)

        # 设备唯一MAC地址
        self.device_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF'
        self.e.add_peer(self.device_mac)

    def on(self):
        self.sta.active(True)
        self.e.active(True)

    def off(self):
        self.e.active(False)
        self.sta.active(False)

    def send(self, msg):
        try:
            self.e.send(self.device_mac, json.dumps({"code": self.code, "msg": msg}))
        except OSError as err:
            if len(err.args) < 2:
                raise err
            if err.args[1] == 'ESP_ERR_ESPNOW_NOT_INIT':
                self.e.active(True)
                self.send(msg)
            elif err.args[1] == 'ESP_ERR_ESPNOW_NOT_FOUND':
                self.e.add_peer(self.device_mac)
                self.send(msg)
            elif err.args[1] == 'ESP_ERR_ESPNOW_IF':
                self.sta.active(True)
                self.send(msg)
            else:
                raise err

    def recv(self):
        back = self.msg
        self.msg = None
        return back

    def callback(self, e):
        msg = self.e.irecv()
        msg = msg[1].decode()
        data = json.loads(msg)
        if data.get('code', None) == self.code:
            self.msg = data.get('msg', None)
            self.func()

    def setcb(self, func):
        self.e.irq(self.callback)
        self.func = func
