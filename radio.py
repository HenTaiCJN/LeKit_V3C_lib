import network
import espnow
import time
actions={'ra':[]}
def raaction(self):
    try:
        actions['ra'][0]()
    except:
        pass
class radio(object):
    def __init__(self):
        # 初始化Wi-Fi为STA模式
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        self.sta.disconnect()

        # 初始化ESP-NOW
        self.e = espnow.ESPNow()
        self.broadcast_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF'
        self.a=""
    def on(self):
        self.sta.active(True)
        self.e.active(True)
        self.e.add_peer(self.broadcast_mac)
    def off(self):
        slef.e.active(False)
        self.sta.active(False)
    def config(self,_ch):
        self.sta.config(channel=_ch)
    def send(self,a):
        self.e.publish(self.broadcast_mac, a)
        time.sleep(0.01)
    def rec(self):
        self.a=""
        self.a=self.e.recv()
        return self.a[1].decode()
    def setcb(self,function):
        try:
            actions['ra']=[function]
            return True
        except:
            print("un-existed function")
    def irq(self):
        self.e.irq(raaction)
        
