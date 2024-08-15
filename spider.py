import requests
from con import data_url
import json
from urllib3.exceptions import InsecureRequestWarning 
# login_url='https://qiu.binance.works/login'
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6ImwxMjQzNjc1MTQ5QGdtYWlsLmNvbSIsIlJvbGUiOjEsIlVzZXJJZCI6IlVORTMxMjlGQzYxOENCMEYzMTFDNzRBOEFDRkJFOTI0REEiLCJleHAiOjE3MjU1NDMzNDF9.FKMIPl0z4pjAuJi4p_IZXWZQKOPLw-BZD9QgVBqojd8",
    "content-type": "application/json",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "i18next=zh-CN",
    "Referer": "https://qiu.binance.works/main-strategy/hft-robots?pageNo=1&pageSize=100&sortField=currentBalance&getListType=INIT&strategies=Dino",
    "Referrer-Policy": "strict-origin-when-cross-origin"}
payload = {
        "pageNo": 1,
        "pageSize": 100,
        "sortField": "currentBalance",
        "getListType": "LOOP",
        "strategies": ["Dino"],
        "ids": [
            "efa4c6bb-2252-4bfe-9077-6d6ac992cd1f", "93b0c313-3fa4-4d51-a4dd-31fdef16d09f",
            # Add the rest of your IDs here...
        ]
    }

session=requests.Session()
response=session.post(data_url,verify=False,json=payload,headers=headers)
if response.status_code == 200:
    r=response.json()
    print(json.dumps(r))
    print(r['data'])
    # print(r)
    print('login success')
else:
    print(response)
    print('login fail')

