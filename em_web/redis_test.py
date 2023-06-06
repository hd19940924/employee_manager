# _*_coding:utf-8_*_
# @Author :hd
# @time :2023/6/6 16:04
# @filename :redis_test.py
# 开发工具 ：PyCharm
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client.set('test_key', 'test_value')
result = redis_client.get('test_key')
print(result)