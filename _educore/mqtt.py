import gc
import random

from machine import Timer

import umqtt.robust as mqtt


class MQTTClient:
    lock = False
    cnt = 0
    _connected = False
    client = None

    msg_list = {}
    callbackList = {}  # user's func

    def __init__(self):
        pass

    @classmethod
    def connect(cls, server, port, client_id='', user='', psd=''):
        if client_id == '':
            alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            client_id = ''.join([alphabet[random.randint(0, len(alphabet) - 1)] for _ in range(6)])

        cls.client = mqtt.MQTTClient(client_id=client_id, server=server, port=port, user=user, password=psd,
                                     keepalive=60)
        try:
            cls.client.connect()
        except Exception as e:
            print('连接失败，请检查wifi是否开启')
            return

        cls._connected = True
        print('mqtt服务器连接成功')
        cls.client.set_callback(cls.callback)
        Timer(3).init(period=100, mode=Timer.PERIODIC, callback=cls.check_msg)
        gc.collect()

    @classmethod
    def connected(cls):
        return cls._connected

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.disconnect()

    @classmethod
    def publish(cls, topic, content):
        cls.lock = True
        try:
            cls.client.publish(topic, content.encode('utf-8'))
            print('推送成功')
        except Exception as e:
            print('推送失败')
        finally:
            cls.lock = False

    @classmethod
    def subscribe(cls, topic):
        cls.lock = True
        try:
            cls.client.subscribe(topic)
            print('订阅成功')
        except Exception as e:
            print('订阅失败')
        finally:
            cls.lock = False

    @classmethod
    def check_msg(cls, a):
        cls.msg_list = {}
        cls.cnt += 1
        if not cls.lock:
            try:
                cls.client.check_msg()
            except Exception as e:
                print('MQTT check msg error:' + str(e))
                return
        if cls.cnt == 200:
            cls.cnt = 0
            try:
                cls.client.ping()  # 心跳消息
                cls._connected = True
            except Exception as e:
                print('MQTT keepalive ping error:' + str(e))
                cls._connected = False

    @classmethod
    def callback(cls, topic, msg):
        gc.collect()
        topic = topic.decode('utf-8', 'ignore')
        msg = msg.decode('utf-8', 'ignore')
        cls.msg_list[topic] = msg

        func = cls.callbackList.get(topic, None)
        if func is not None:
            func()

    @classmethod
    def receive(cls, topic):
        msg = cls.msg_list.get(topic, None)
        return msg

    @classmethod
    def Received(cls, topic, callback):
        cls.subscribe(topic)
        cls.callbackList[topic] = callback
