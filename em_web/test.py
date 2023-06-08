# _*_coding:utf-8_*_
# @Author :hd
# @time :2023/5/24 11:43
# @filename :test.py
# 开发工具 ：PyCharm
import models
from datetime import datetime
date_str = '2023-06-08 16:00:00+00:00'
date_format = '%Y-%m-%d %H:%M:%S%z'
date_obj = datetime.strptime(date_str, date_format)
print(date_obj)
