from django.db import models

# Create your models here.
class Department(models.Model):
    dep_name=models.CharField(verbose_name="部门名称",max_length=32)
    def __str__(self):
        return self.dep_name
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
    dep=models.ForeignKey(to="Department",to_field="id",on_delete=models.CASCADE)

