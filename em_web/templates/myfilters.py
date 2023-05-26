# _*_coding:utf-8_*_
# @Author :hd
# @time :2023/5/25 11:45
# @filename :myfilters.py.py
# 开发工具 ：PyCharm
from jinja2 import Environment
from django import template
register = template.Library()
@register.filter
def str_filter(value):
    return str(value)
@register.filter
def full_name(user):
    return user.first_name + ' ' + user.last_name
#env = Environment()
#env.filters['str'] = str_filter

# 现在可以在模板中使用 'str' 过滤器了