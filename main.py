from model import JudgeManger

if __name__=='__main__':
    # rd=RobotData(1,100)
    # rm=RobotManager(1,100)
    # rm.change_open_range(1,100)
    # print(rm.grouped_ids[1][0])
    # aa=AutoAdjust()
    # aa.init_group(1,'sol_usdt')
    jm=JudgeManger(1,100)
    # jm.calculate_and_store_profit_rate(id=1)
    jm.print_balance_history()