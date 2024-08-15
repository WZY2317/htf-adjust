import requests
import urllib3
urllib3.disable_warnings()
from con import headers,update_url
from model import  ChangeParamsPayload
session=requests.Session()
pay_load=ChangeParamsPayload(taskUid='4217bf19-d00d-4fd3-ada5-a3c364c71434')
pay_load.change_open(new_open=15)
print(pay_load.to_dict())
response = session.post(url=update_url, json=pay_load.to_dict(), headers=headers, verify=False)
if response.status_code==200:
    print(response.text)
else:
    print(response.text)

