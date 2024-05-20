import gc
import json
import random

import umqtt.robust as mqtt

from _educore._timer import _timer


class webcamera:
    id = None
    lock = False
    cnt = 0
    _connected = False
    client = None
    callback_func=None
    res= '{}'
    msg_list = {}

    class fcr:
        id = None
        blinks = None
        mouth = None

    def __init__(self):
        pass

    @classmethod
    def receivedfunction(cls):
        msg = cls.receive(topic=cls.id)
        cls.res=msg
        status = json.loads(msg).get('status', None)
        if status:
            webcamera.fcr.id = json.loads(msg).get('id', None)
        else:
            webcamera.fcr.id = None
        webcamera.fcr.blinks = json.loads(msg).get('blink', None)
        webcamera.fcr.mouth = json.loads(msg).get('mouth_open', None)
        gc.collect()

    @classmethod
    def result(cls):
        return cls.res
    @classmethod
    def connect(cls, id):
        cls.id = id
        cls.lock = False
        cls._connected = False
        cls.callback_func = None  # user's func
        cls.cnt = 0

        if id is None:
            print('请输入id')
            return
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        random_str = ''.join([alphabet[random.randint(0, len(alphabet) - 1)] for _ in range(6)])

        cls.connect_mqtt('cloud.leihoorobot.com', 1883, random_str)

    @classmethod
    def connect_mqtt(cls, server, port, client_id, user='', psd=''):
        cls.client = mqtt.MQTTClient(client_id=client_id, server=server, port=port, user=user, password=psd,
                                     keepalive=60)
        try:
            cls.client.connect()
        except Exception as e:
            print('连接失败，请检查wifi是否开启')
            return

        print('webcamera连接成功')
        cls.client.set_callback(cls.callback)
        _timer.add(cls.check_msg, 100)

        gc.collect()
        cls.Received(topic=cls.id, callback=cls.receivedfunction)

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
    def check_msg(cls):
        webcamera.msg_list = {}
        cls.cnt += 1
        if not cls.lock:
            try:
                cls.client.check_msg()
            except Exception as e:
                print('MQTT check msg error:' + str(e))
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
        topic = topic.decode('utf-8')
        msg = msg.decode('utf-8')
        webcamera.msg_list[topic] = msg
        cls.callback_func()

    @classmethod
    def receive(cls, topic):
        msg = webcamera.msg_list.get(topic, None)
        return msg

    @classmethod
    def Received(cls, topic, callback):
        cls.client.subscribe(topic)
        cls.callback_func = callback