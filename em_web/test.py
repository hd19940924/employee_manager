# _*_coding:utf-8_*_
# @Author :hd
# @time :2023/5/24 11:43
# @filename :test.py
# 开发工具 ：PyCharm
import models
"""from datetime import datetime
date_str = '2023-06-08 16:00:00+00:00'
date_format = '%Y-%m-%d %H:%M:%S%z'
date_obj = datetime.strptime(date_str, date_format)
print(date_obj)"""
import requests

url = "http://127.0.0.1:8000/login/"

payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n123456\r\n-----011000010111000001101001--\r\n\r\n"
headers = {"content-type": "multipart/form-data; boundary=---011000010111000001101001"}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)