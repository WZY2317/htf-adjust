import json
from urllib3.exceptions import InsecureRequestWarning
from con import data_url,headers,update_url
import requests
import time
import sqlite3
from dataclasses import dataclass
from typing import List, Optional
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@dataclass
class StrateParams:
    close:int
    close_range:int
    expert_mode:bool
    lever:int
    main_ref_index:str
    open:int
    open_range:int
    pair:str
    price_bar:str
    ref_exchange:str
    ref_pair:str
    stop_loss:float

@dataclass
class ServerInfo:
    cpu: str
    ipPool: int
    mem: int
    memPct: str
    diskPct: str
    taskNum: int
    straVersion: bool
    straVersionDetail: Optional[str]

@dataclass
class Server:
    ID: int
    CreatedAt: str
    UpdatedAt: str
    DeletedAt: Optional[str]
    nickname: str
    ip: str
    innerIp: str
    port: str
    Operator: str
    MachineID: str
    remark: str
    vpcId: str
    serverInfo: ServerInfo

@dataclass
class Account:
    ID: int
    CreatedAt: str
    UpdatedAt: str
    DeletedAt: Optional[str]
    nickname: str
    exchangeName: str
    originAccount: str
    apiKey: str
    brokerId: str
    Operator: str
    remark: str
    accountType: int
    applyTime: int
    isCombined: bool
    isMulti: bool
    accountIDs: Optional[List[int]]
    apiType: int

@dataclass
class Strategy:
    ID: int
    CreatedAt: str
    UpdatedAt: str
    DeletedAt: Optional[str]
    strategyName: str
    strategyNickname: str

@dataclass
class TradingTask:
    id: str
    nickname: str
    creator: str
    createTime: int
    initBalance: float
    strategyParams: StrateParams
    server: Server
    serverId: int
    accountId: int
    account: Account
    strategyId: int
    strategy: Strategy
    taskUid: str
    status: int
    currentBalance: float
    exitMsg: str
    serverStatus: int
    yield_: float
    lastRunTime: str
    lastResetTime: str
    autoRestart: bool
    strategyVersion: str
    colo: bool
    bus: bool
    pri: bool
    logLevel: str
    taskMsg: str
    watch: bool
    model: bool
    lastStopTime: str
    remark: str
    pin: bool
    needUpdate: bool
    currVersion: str
    tradeExValue: float
    refExValue: float
    tradeVal: str
    pnlPct: float
    errMsg: List[str]
    lastVersion: bool
    volume: float
    cash: float
    cashPnl: float
    arbitragePnl: float
    busBulb: bool
    currencyRatio: float
    forceRestart: bool
    coin: float
    locked: bool
    strategyParam:StrateParams

class ChangeParamsPayload:
    def __init__(self,pageNo, pageSize,id):
        #每次改变参数的时候都获取一遍原本的参数,从原本的参数的基础上去改动
        self.data_base = DataManager(pageNo, pageSize)
        stategy_task=self.data_base.id_data[id]
        self.accountId = stategy_task.accountId
        self.autoRestart = stategy_task.autoRestart
        self.autoRestartIds = []
        self.id=stategy_task.id
        self.initBalance = None
        self.logLevel = stategy_task.logLevel
        self.nickname=stategy_task.nickname
        self.serverId = stategy_task.serverId
        self.strategyId=stategy_task.strategyId
        # 解析 JSON 字符串为字典
        strategy_params_dict = json.loads(stategy_task.strategyParams)

        #将字典转换为 StrateParams 对象
        self.strategyParams = StrateParams(
            open=strategy_params_dict["open"],
            open_range=strategy_params_dict["open_range"],
            close=strategy_params_dict["close"],
            close_range=strategy_params_dict["close_range"],
            stop_loss=strategy_params_dict["stop_loss"],
            lever = strategy_params_dict["lever"],
            pair=strategy_params_dict["pair"],
            ref_exchange=strategy_params_dict["ref_exchange"],
            ref_pair=strategy_params_dict["ref_pair"],
            main_ref_index=strategy_params_dict["main_ref_index"],
            price_bar=strategy_params_dict["price_bar"],
            expert_mode=strategy_params_dict["expert_mode"]
        )
    def change_open(self, new_open):
        self.strategyParams.open= new_open

    def change_open_range(self, new_open_range):
        self.strategyParams.open_range = new_open_range
    def change_open_symbol(self,new_pair):
        self.strategyParams.pair = new_pair
    def change_refer_symbol(self,refer_pair):
        pair = "{}|{}".format(refer_pair, refer_pair)
        self.strategyParams.ref_pair= pair
    def to_json(self):
        # Serialize strategyParams to a JSON string
        strategy_params_str = json.dumps({
            "open": self.strategyParams.open,
            "open_range": self.strategyParams.open_range,
            "close": self.strategyParams.close,
            "close_range": self.strategyParams.close_range,
            "stop_loss": self.strategyParams.stop_loss,
            "lever": self.strategyParams.lever,
            "pair": self.strategyParams.pair,
            "ref_exchange": self.strategyParams.ref_exchange,
            "ref_pair": self.strategyParams.ref_pair,
            "main_ref_index": self.strategyParams.main_ref_index,
            "price_bar": self.strategyParams.price_bar,
            "expert_mode": self.strategyParams.expert_mode,
        }, ensure_ascii=False, separators=(',', ':'))

        # Construct the main dictionary with strategyParams as a JSON string
        data_dict = {
            "nickname": self.nickname,
            "strategyId": self.strategyId,
            "accountId": self.accountId,
            "serverId": self.serverId,
            "logLevel": self.logLevel,
            "autoRestart": self.autoRestart,
            "strategyParams": strategy_params_str,  # This remains a JSON string
            "initBalance": self.initBalance,
            "id": self.id,
            "autoRestartIds": self.autoRestartIds,
        }

        # Return the dictionary itself, not the string representation
        return data_dict
class ParamData:
    def __init__(self,strategyParams:dict):
        self.close=strategyParams['close']
        self.open_range=strategyParams['open_range']
        self.close_range=strategyParams['close_range']
        self.stop_loss=strategyParams['stop_loss']
        self.lever=strategyParams['lever']
        self.main_ref_index=strategyParams['main_ref_index']
        self.price_bar=strategyParams['price_bar']
        self.pair=strategyParams['pair']
        self.ref_pair=strategyParams['ref_pair']
class AccountData:
    def __init__(self,accountParams:dict):
        self.ID=accountParams['ID'],
        self.nickname=accountParams['nickname'],
        self.exchangeName=accountParams['exchangeName'],

class RobotData:
    def __init__(self, pageNo, pageSize):
        self.robot_data = {}#task_id 对应的 数据
        self.id_data={}#account 和对应的数据
        self.account_data={}
        pay_load = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "sortField": "currentBalance",
            "getListType": "INIT",
            "strategies": ["Dino"],
        }
        session = requests.Session()
        response = session.post(data_url, headers=headers, json=pay_load, verify=False)

        if response.status_code == 200:
            data = response.json()
            self.count =data['data']['count']
            strategy_list = data.get('data', {}).get('list', [])

            for strategy in strategy_list:
                if isinstance(strategy, dict):
                    strategy_id = strategy.get('id')
                    strategy_params = strategy.get('strategyParams')
                    account_params=strategy.get('account')
                    strategy_Id=strategy.get('strategyId')#类似 1,2,3
                    if strategy_id and strategy_params:
                        self.robot_data[strategy_id] = ParamData(json.loads(strategy_params))
                        self.id_data[strategy_Id] = strategy_id
                        self.account_data[strategy_Id] = AccountData(json.loads(account_params))

                else:
                    print(f"Unexpected data structure: {strategy}")
        else:
            print(f"Failed to fetch data: {response.status_code}")


class RobotManager:#用于改参的类
    def __init__(self, pageNo, pageSize):
        self.data_base=DataManager(pageNo, pageSize)
        self.pageNo=pageNo
        self.pageSize=pageSize
        self.session = requests.Session()
        self.process_count()#从第1组开始  0 1 2 3 个账号
    def change_open(self,id,new_open):#id是第几个策略,num是调到几
        pay_load=ChangeParamsPayload(self.pageNo, self.pageSize,id)
        pay_load.change_open(new_open)
        response = self.session.post(update_url, headers=headers, json=pay_load.to_json(), verify=False)
        print(response.text)
        return response.status_code
    def change_open_range(self,id,new_open):
        pay_load=ChangeParamsPayload(self.pageNo, self.pageSize,id)
        pay_load.change_open_range(new_open)
        response = self.session.post(update_url, headers=headers, json=pay_load.to_json(), verify=False)
        print(response.text)
        return response.status_code
    def change_symbol(self,id,new_symbol):
        pay_load = ChangeParamsPayload(self.pageNo, self.pageSize, id)
        pay_load.change_open_symbol(new_symbol)#改变交易对
        pay_load.change_refer_symbol(new_symbol)#改变参考交易对
        response = self.session.post(update_url, headers=headers, json=pay_load.to_json(), verify=False)
        print(response)
        return response.status_code
    def init_params(self,id,pair):
        code1 = self.change_open(id,8)
        code2= self.change_open_range(id,10)#初始化参数是 8 和 10
        code3 =self.change_symbol(id,pair)
        print(code1,code2,code3)

    def process_count(self):
        count_list = [id for id in range(1, self.data_base.count + 1)]
        grouped_ids = [count_list[i:i + 4] for i in range(0, len(count_list), 4)]
        adjusted_grouped_ids = {}
        for idx, group in enumerate(grouped_ids, start=1):
            adjusted_grouped_ids[idx] = group
        self.grouped_ids=adjusted_grouped_ids



class DataManager:#用于初始化收取数据的类
    def __init__(self, pageNo, pageSize):
        self.task_data = {}
        self.id_data={}
        pay_load = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "sortField": "currentBalance",
            "getListType": "INIT",
            "strategies": ["Dino"],
        }
        session = requests.Session()
        response = session.post(data_url, headers=headers, json=pay_load, verify=False)

        if response.status_code == 200:
            data = response.json()
            self.count = data['data']['count']
            strategy_list = data.get('data', {}).get('list', [])
            for strategy in strategy_list:
                if isinstance(strategy, dict):
                    task_id = strategy.get('id')
                    strategy_id = strategy.get('strategyId')
                    id=strategy['accountId'],
                    strategy_params_dict = json.loads(strategy['strategyParams'])
                    strategy_param = StrateParams(
                        close=strategy_params_dict['close'],
                        close_range=strategy_params_dict['close_range'],
                        expert_mode=strategy_params_dict['expert_mode'],
                        lever=strategy_params_dict['lever'],
                        main_ref_index=strategy_params_dict['main_ref_index'],
                        open=strategy_params_dict['open'],
                        open_range=strategy_params_dict['open_range'],
                        pair=strategy_params_dict['pair'],
                        price_bar=strategy_params_dict['price_bar'],
                        ref_exchange=strategy_params_dict['ref_exchange'],
                        ref_pair=strategy_params_dict['ref_pair'],
                         stop_loss=strategy_params_dict['stop_loss']
                    )
                    # Constructing the structures based on the provided strategy data
                    server_info = ServerInfo(
                        cpu=strategy['server']['serverInfo']['cpu'],
                        ipPool=strategy['server']['serverInfo']['ipPool'],
                        mem=strategy['server']['serverInfo']['mem'],
                        memPct=strategy['server']['serverInfo']['memPct'],
                        diskPct=strategy['server']['serverInfo']['diskPct'],
                        taskNum=strategy['server']['serverInfo']['taskNum'],
                        straVersion=strategy['server']['serverInfo']['straVersion'],
                        straVersionDetail=strategy['server']['serverInfo']['straVersionDetail']
                    )

                    server = Server(
                        ID=strategy['server']['ID'],
                        CreatedAt=strategy['server']['CreatedAt'],
                        UpdatedAt=strategy['server']['UpdatedAt'],
                        DeletedAt=strategy['server']['DeletedAt'],
                        nickname=strategy['server']['nickname'],
                        ip=strategy['server']['ip'],
                        innerIp=strategy['server']['innerIp'],
                        port=strategy['server']['port'],
                        Operator=strategy['server']['Operator'],
                        MachineID=strategy['server']['MachineID'],
                        remark=strategy['server']['remark'],
                        vpcId=strategy['server']['vpcId'],
                        serverInfo=server_info
                    )

                    account = Account(
                        ID=strategy['account']['ID'],
                        CreatedAt=strategy['account']['CreatedAt'],
                        UpdatedAt=strategy['account']['UpdatedAt'],
                        DeletedAt=strategy['account']['DeletedAt'],
                        nickname=strategy['account']['nickname'],
                        exchangeName=strategy['account']['exchangeName'],
                        originAccount=strategy['account']['originAccount'],
                        apiKey=strategy['account']['apiKey'],
                        brokerId=strategy['account']['brokerId'],
                        Operator=strategy['account']['Operator'],
                        remark=strategy['account']['remark'],
                        accountType=strategy['account']['accountType'],
                        applyTime=strategy['account']['applyTime'],
                        isCombined=strategy['account']['isCombined'],
                        isMulti=strategy['account']['isMulti'],
                        accountIDs=strategy['account']['accountIDs'],
                        apiType=strategy['account']['apiType']
                    )

                    strategy_obj = Strategy(
                        ID=strategy['strategy']['ID'],
                        CreatedAt=strategy['strategy']['CreatedAt'],
                        UpdatedAt=strategy['strategy']['UpdatedAt'],
                        DeletedAt=strategy['strategy']['DeletedAt'],
                        strategyName=strategy['strategy']['strategyName'],
                        strategyNickname=strategy['strategy']['strategyNickname']
                    )

                    trading_task = TradingTask(
                        id=task_id,
                        nickname=strategy['nickname'],
                        creator=strategy['creator'],
                        createTime=strategy['createTime'],
                        initBalance=strategy['initBalance'],
                        strategyParams=strategy['strategyParams'],
                        server=server,
                        strategyParam=strategy_param,
                        serverId=strategy['serverId'],
                        accountId=strategy['accountId'],
                        account=account,
                        strategyId=strategy_id,
                        strategy=strategy_obj,
                        taskUid=strategy['taskUid'],
                        status=strategy['status'],
                        currentBalance=strategy['currentBalance'],
                        exitMsg=strategy['exitMsg'],
                        serverStatus=strategy['serverStatus'],
                        yield_=strategy['yield'],
                        lastRunTime=strategy['lastRunTime'],
                        lastResetTime=strategy['lastResetTime'],
                        autoRestart=strategy['autoRestart'],
                        strategyVersion=strategy['strategyVersion'],
                        colo=strategy['colo'],
                        bus=strategy['bus'],
                        pri=strategy['pri'],
                        logLevel=strategy['logLevel'],
                        taskMsg=strategy['taskMsg'],
                        watch=strategy['watch'],
                        model=strategy['model'],
                        lastStopTime=strategy['lastStopTime'],
                        remark=strategy['remark'],
                        pin=strategy['pin'],
                        needUpdate=strategy['needUpdate'],
                        currVersion=strategy['currVersion'],
                        tradeExValue=strategy['tradeExValue'],
                        refExValue=strategy['refExValue'],
                        tradeVal=strategy['tradeVal'],
                        pnlPct=strategy['pnlPct'],
                        errMsg=strategy['errMsg'],
                        lastVersion=strategy['lastVersion'],
                        volume=strategy['volume'],
                        cash=strategy['cash'],
                        cashPnl=strategy['cashPnl'],
                        arbitragePnl=strategy['arbitragePnl'],
                        busBulb=strategy['busBulb'],
                        currencyRatio=strategy['currencyRatio'],
                        forceRestart=strategy['forceRestart'],
                        coin=strategy['coin'],
                        locked=strategy['locked']
                    )

                    # Store the data
                    self.id_data[id[0]] = trading_task
                    self.task_data[task_id[0]] = trading_task

class JudgeManger:
    def __init__(self,pageNo,pageSize):
        self.data_base = DataManager(pageNo, pageSize)

    def create_table(self, db_path='balance.db'):
        with sqlite3.connect(db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS balance_history (
                    id TEXT,
                    taskUid TEXT,
                    nickname TEXT,
                    pair TEXT,
                    timestamp REAL,
                    balance REAL,
                    profit_rate REAL,
                    PRIMARY KEY (id, timestamp)
                )
            ''')

    def store_profit_rate(self, id, balance, taskUid, nickname, pair, profit_rate, db_path='balance.db'):
        with sqlite3.connect(db_path) as conn:
            conn.execute('''
                   INSERT INTO balance_history (id, taskUid, nickname, pair, timestamp, balance, profit_rate) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)
               ''', (id, taskUid, nickname, pair, time.time(), balance, profit_rate))
        print("插入数据成功")
    def get_last_balance(self, id, db_path='balance.db'):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT balance, timestamp FROM balance_history WHERE id = ? ORDER BY timestamp DESC LIMIT 1', (id,))
            return cursor.fetchone()

    def calculate_and_store_profit_rate(self, id, db_path='balance.db'):
        strategy_task = self.data_base.id_data[id]
        strategy_params_dict = json.loads(strategy_task.strategyParams)
        current_balance = strategy_task.currentBalance
        taskUid = strategy_task.taskUid
        nickname = strategy_task.nickname
        pair = strategy_params_dict['pair']

        self.create_table(db_path)  # 确保表已创建

        last_record = self.get_last_balance(id, db_path)
        if last_record:
            last_balance, last_timestamp = last_record
            elapsed_time = time.time() - last_timestamp

            if elapsed_time >= 4 * 3600:  # 4小时的秒数
                profit_rate = ((current_balance - last_balance) / last_balance) * 100
                print(f"ID {id} ({nickname}, {pair}) 的4小时收益率: {profit_rate}%")

                # 存储当前余额、收益率和其他信息
                self.store_profit_rate(id, current_balance, taskUid, nickname, pair, profit_rate, db_path)
            else:
                print("距离上次记录还没有过4个小时。")
        else:
            # 第一次记录, 没有收益率
            self.store_profit_rate(id, current_balance, taskUid, nickname, pair, None, db_path)
            print(f"ID {id} ({nickname}, {pair}) 的初始余额已记录。")

    def get_last_profit_rate(self, id, db_path='balance.db'):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT profit_rate FROM balance_history WHERE id = ? ORDER BY timestamp DESC LIMIT 1',
                           (id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def print_balance_history(self, db_path='balance.db'):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM balance_history ORDER BY timestamp')
            records = cursor.fetchall()
            for record in records:
                print(f"ID: {record[0]}, TaskUID: {record[1]}, Nickname: {record[2]}, Pair: {record[3]}, "
                      f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record[4]))}, "
                      f"Balance: {record[5]}, Profit Rate: {record[6]}")
