import gc
import time

from machine import Timer


class __timer:
    def __init__(self):
        self.timer_list = []
        Timer(2).init(period=500, mode=Timer.PERIODIC, callback=self.timer3Run)

    def add(self, func, period, delay=None):
        self.timer_list.append({"func": func, "period": period, "lastRun": 0, "delay": delay})

    def delete(self, func):
        for i in self.timer_list:
            if i["func"] == func:
                self.timer_list.remove(i)
                break

    def timer3Run(self, v):
        gc.collect()
        current_time = time.time_ns() // 1000000
        for timer in self.timer_list:
            # 检查是否达到定时周期
            if current_time - timer["lastRun"] < timer["period"]:
                continue  # 时间未到，跳过本次循环

            # 检查是否存在延迟，并处理延迟逻辑
            if timer["delay"] is not None:
                if timer["lastRun"] == 0:  # 第一次运行
                    timer["lastRun"] = current_time
                    timer["func"]()  # 执行函数
                    continue

                # 更新延迟时间
                timer["delay"] -= current_time - timer["lastRun"]
                if timer['delay'] <= 0:  # 延迟时间已达到，移除定时器
                    self.timer_list.remove(timer)
                    continue

            # 更新上次运行时间并执行函数
            timer["lastRun"] = current_time
            timer["func"]()


_timer = __timer()

# def timer3Run(self, v):
#     gc.collect()
#     for i in self.timer_list:
#         nowTime = time.time_ns() // 1000000
#         if nowTime - i["lastRun"] >= i["period"]:
#             if i["delay"] is not None:
#                 if not i["lastRun"] == 0:  # lastRun=0,means the first time run
#                     i["delay"] -= nowTime - i["lastRun"]
#                     if i['delay'] <= 0:
#                         self.timer_list.remove(i)
#                         continue
#             i["lastRun"] = nowTime
#             i["func"]()
