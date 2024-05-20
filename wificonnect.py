import network
import time

wlan = network.WLAN(network.STA_IF)


def start():
    wlan.active(True)
    if wlan.isconnected():
        wlan.disconnect()
    print("WLAN start successed")


def scan():
    wlan_imformation = wlan.scan()
    print("WLAN scan successed")
    return wlan_imformation


def connect(ssid, password, timeout=10000):
    if wlan.isconnected():
        wlan.disconnect()

    timeout = timeout / 1000  # 设置超时时间为30秒

    start_time = time.time()

    print("WLAN Connecting")
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        if wlan.isconnected():
            break
        if time.time() - start_time > timeout:
            print("WLAN Connect Timeout")
            close()
            return

    if wlan.isconnected():
        print("WLAN Connect Successd")
    else:
        print("WLAN Connect Failed")
        close()


def close():
    if wlan.isconnected():
        wlan.disconnect()
    wlan.active(False)


def status():
    if wlan.isconnected():
        return True
    return False


def info():
    if not wlan.isconnected():
        print('wifi not connected')
        return
    return wlan.ifconfig()
