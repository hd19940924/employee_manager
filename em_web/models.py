from django.db import models

# Create your models here.
class Department(models.Model):
    dep_name=models.CharField(verbose_name="部门名称",max_length=32)
    def __str__(self):
       return self.dep_name
    def employee_count(self):
        return Employee.objects.filter(dep=self).count()

class Employee(models.Model):
    name=models.CharField(verbose_name="员工姓名",max_length=16)
    password=models.CharField(verbose_name="员工密码",max_length=64)
    age=models.IntegerField(verbose_name="员工年龄")
    account=models.DecimalField(verbose_name="账户余额",max_digits=10, decimal_places=2,default=0)
    create_time=models.DateTimeField(verbose_name="入职时间")
    gender_choices=(
        (1,"男"),
        (2,"女"),
    )
    gender= models.SmallIntegerField(verbose_name="员工性别",choices=gender_choices)
    dep=models.ForeignKey(to="Department",to_field="id",related_name='employees',on_delete=models.CASCADE)

class detection_collect(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, null=True)
    url = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=100, null=True)
    time = models.DateTimeField(auto_now_add=True)
# models.py 文件
class Person(models.Model):
    # 姓名 str类型
    name = models.CharField(max_length=20,verbose_name='姓名')
    # 年龄 int型
    age=models.IntegerField(verbose_name='年龄')
    # 成绩 float类型
    score = models.FloatField(verbose_name='成绩')
from django.db import models

class LoginUser(models.Model):
    name = models.CharField(max_length=16,verbose_name='用户名')
    pwd = models.CharField(max_length=16,verbose_name='密码')

    def __str__(self):
        return self.name


from django.db import models
class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    age = models.IntegerField()



