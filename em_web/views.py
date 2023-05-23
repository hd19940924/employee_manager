import datetime
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import  messages
# from models import models
from em_web import models
from django.core.paginator import Paginator
from django.shortcuts import render


# Create your views here.
def login(request):
    if (request.method == "GET"):
        return render(request, "login.html")
    elif request.method == "POST":
        post_data = request.POST
        print(post_data)
        name = request.POST.get("username")
        print(name)
        password = request.POST.get("password")
        print(password)
        if (name == "admin" and password == "123456"):
            response=redirect("/dep_list")
            response.set_cookie('name', name,max_age=60)
            return response
            # return  HttpResponse("登录成功")
        messages.error(request, '用户名或密码错误！')
        return render(request, "login.html", {"error": "用户名或密码错误！"})

def dep_list(request):
     all_dept=models.Department.objects.all()

     return render(request,"dep_list.html",{"all_depts":all_dept})

def query_dep(request):
    dep_name=request.GET.get("dep_name")
    dep=models.Department.objects.filter(Q(dep_name=dep_name))
    return render(request,"dep_list.html",{"all_depts":dep})

def dep_add(request):

        if request.method == "GET":
           return render(request,"dep_add.html")
        elif request.method == "POST":
            dep_name = request.POST.get("dep_name")
            models.Department.objects.create(dep_name=dep_name)
            return redirect("http://127.0.0.1:8000/dep_list/")
def dep_del(request):
    del_id=request.GET.get("del_id")
    models.Department.objects.filter(id=del_id).delete()
    return  redirect("/dep_list/")

def dep_update(request):
    update_dep_id= None
    if request.method=="GET":
        update_dep_id=request.GET.get("update_id")
        default_dep= models.Department.objects.filter(id=update_dep_id).first()
        return render(request,"dep_update.html",{
            "default_dep":default_dep
        })
    elif request.method =="POST":
        new_dep_id = request.POST.get("new_dep_id")
        new_dep_name= request.POST.get("new_dep_name")
        models.Department.objects.filter(id=new_dep_id).update(dep_name=new_dep_name)
        return redirect("/dep_list/")
def emp_list(request):
    all_emp_data=models.Employee.objects.all()
    for emp in all_emp_data:
        emp.create_time=emp.create_time.strftime("%Y-%m-%d")
        emp.gender=emp.get_gender_display()
        emp.dep_id=models.Department.objects.filter(id=emp.dep_id).first()
    return render(request,"emp_list.html",{"emp_queryset":all_emp_data})
def china(request):
    return render(request,"china.html")
def world(request):
    return render(request,"world.html")
def my_view(request):
    my_objects = models.Department.objects.all()
    paginator = Paginator(my_objects, 2) # 分页，每页显示25条数据
    page = request.GET.get('page')
    my_objects = paginator.get_page(page) # 获取指定页数的数据
    return render(request, 'page.html', {'my_objects': my_objects})
def my_NewView(request):
    my_objects = models.Department.objects.all()
    page_size = request.GET.get('per_page') or 2 # 默认每页显示2条
    paginator = Paginator(my_objects, page_size)
    page = request.GET.get('page')
    my_objects = paginator.get_page(page)

    return render(request, 'my_Newtemplate.html', {
        'my_objects': my_objects,
        'page_sizes': [2, 5, 10], # 定义可选的每页条数
    })