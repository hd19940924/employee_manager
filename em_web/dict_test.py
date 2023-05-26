# _*_coding:utf-8_*_
# @Author :hd
# @time :2023/5/25 10:46
# @filename :dict_test.py
# 开发工具 ：PyCharm
dict1={}
dict1["name"]="hd123"
print(dict1)
print(dict1["name"])
print(type(dict1["name"]))
student = {'name': 'David', 'age': 20, 'gender': 'male'}
str_dict = {k: str(v) for k, v in student.items()}
print(str_dict)
for k, v in student.items():
    student[k] = str(v)

print(student)