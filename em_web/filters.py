# _*_coding:utf-8_*_
# @Author :hd
# @time :2023/5/25 11:04
# @filename :filters.py.py
# 开发工具 ：PyCharm
from jinja2 import Environment

def str_filter(value):
    return str(value)

env = Environment()
env.filters['str'] = str_filter