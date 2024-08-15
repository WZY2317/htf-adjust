from model import *
class AutoAdjust:
    def __init__(self):
        pass
    def init_group(self,group_id,symbol):#初始化四个相同参数的机器人
        rm = RobotManager(1, 100)
        for i in range(4):
            rm.init_params(rm.grouped_ids[group_id][i],symbol)





