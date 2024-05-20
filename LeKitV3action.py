from machine import Timer,Pin
import time
Touch_Pin1=Pin(18, Pin.IN)
Touch_Pin2=Pin(5, Pin.IN)
que=[["",0],["",0],["",0]]
start_time=time.ticks_ms()
actions={'key_A_click':[],'key_A_dclick':[],'key_A_press':[],
        'key_B_click':[],'key_B_dclick':[],'key_B_press':[],
        'slide_up':[],'slide_down':[],'dlongclick':[]}
'按键事件绑定'
def setcb(action,function):
    if not action in actions:
        print("%s error!action name must in key_A_click,key_A_dclick,key_A_press,key_B_click,key_B_dclick,key_B_press,slide_up,slide_down"%(action))
        return False
    actions[action]=[function]
    return True
'按键事件解除'
def delcb(action):
    if not action in actions:
        print("%s error!action name must in key_A_click,key_A_dclick,key_A_press,key_B_click,key_B_dclick,key_B_press,slide_up,slide_down"%(action))
        return False
    actions[action]=[]
    return True
'A单击事件'
def t1_click():
#     print('t1_click')
    fs=actions['key_A_click']
    try:
        fs[0]()
    except:
        pass
'A双击事件'
def t1_dclick():
#     print('t1_dclick')
    fs=actions['key_A_dclick']
    try:
        fs[0]()
    except:
        pass
'A滑动事件'
def t1_scroll():
#     print('t1_scroll')
    fs=actions['slide_down']
    try:
        fs[0]()
    except:
        pass
'A长按事件'
def t1_longclick():
#     print('t1_longclick')
    fs=actions['key_A_press']
    try:
        fs[0]()
    except:
        pass

'B单击事件'
def t2_click():
#     print('t2_click')
    fs=actions['key_B_click']
    try:
        fs[0]()
    except:
        pass
'B双击事件'
def t2_dclick():
#     print('t2_dclick')
    fs=actions['key_B_dclick']
    try:
        fs[0]()
    except:
        pass
'B滑动事件'
def t2_scroll():
#     print('t2_scroll')
    fs=actions['slide_up']
    try:
        fs[0]()
    except:
        pass
'B长按事件'
def t2_longclick():
#     print('t2_longclick')
    fs=actions['key_B_press']
    try:
        fs[0]()
    except:
        pass
def dlongclick():
#     print('dlongclick')
    fs=actions['dlongclick']
    try:
        fs[0]()
    except:
        pass
'定时器回调事件'
def clock(self):
    if que[-1][0]=='1d' and time.ticks_ms()-que[-1][1]>2000:
        if Touch_Pin2.value() == 1:
            dlongclick()
        else:
            t1_longclick()
        for i in range(3):
            que.pop(0)
            que.append(["",time.ticks_ms()])
    if (que[-3][0]=='1u' and que[-2][0]=='2d' and que[-1][0]=='2u') or (que[-3][0]=='2d' and que[-2][0]=='1u' and que[-1][0]=='2u'):
        if que[-1][1]-que[-3][1]<300:
            t1_scroll()
#             print(que)
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    if que[-2][0]=='1d' and que[-1][0]=='1u':
        if 200<que[-1][1]-que[-2][1]<1000:
#             print(que)
            t1_click()
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    if que[-3][0]=='1u' and que[-2][0]=='1d' and que[-1][0]=='1u':
        if que[-1][1]-que[-3][1]<300:
#             print(que)
            t1_dclick()
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    #---------------------------------------------------------------
    if que[-1][0]=='2d' and time.ticks_ms()-que[-1][1]>2000:
        if Touch_Pin1.value() == 1:
            dlongclick()
        else:
            t2_longclick()
        for i in range(3):
            que.pop(0)
            que.append(["",time.ticks_ms()])
    if (que[-3][0]=='2u' and que[-2][0]=='1d' and que[-1][0]=='1u') or (que[-3][0]=='1d' and que[-2][0]=='2u' and que[-1][0]=='1u'):
        if que[-1][1]-que[-3][1]<300:
            t2_scroll()
#             print(que)
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    if que[-2][0]=='2d' and que[-1][0]=='2u':
        if 200<que[-1][1]-que[-2][1]<1000:
#             print(que)
            t2_click()
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    if que[-3][0]=='2u' and que[-2][0]=='2d' and que[-1][0]=='2u':
        if que[-1][1]-que[-3][1]<300:
#             print(que)
            t2_dclick()
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
'A触摸回调事件'
def t1(self):
    global que
    if Touch_Pin1.value() == 1:
        que.pop(0)
        que.append(["1d",time.ticks_ms()])
    else:
        que.pop(0)
        que.append(["1u",time.ticks_ms()])
'B触摸回调事件'  
def t2(self):
    if Touch_Pin2.value() == 1:
        que.pop(0)
        que.append(["2d",time.ticks_ms()])
    else:
        que.pop(0)
        que.append(["2u",time.ticks_ms()])


Touch_Pin1.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING,handler =t1)
Touch_Pin2.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING,handler =t2)

Timer(1).init(period=100, mode=Timer.PERIODIC, callback=clock)
'8.30改'
