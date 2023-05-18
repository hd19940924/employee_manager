from django.db import models

# Create your models here.
class Department(models.Model):
    dep_name=models.CharField(verbose_name="部门名称",max_length=32)
class Employee(models.Model):
    name=models.CharField(verbose_name="员工姓名",max_length=16)
    password=models.CharField(verbose_name="员工密码",max_length=64)
    age=models.IntegerField(verbose_name="员工年龄")
    account=models.DateTimeField(verbose_name="账户余额",max_length=10,decimal_places=2,default=0)
    create_time=models.DateTimeField(verbose_name="入职时间")

