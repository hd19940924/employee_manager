import datetime
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import  messages
# from models import models
from em_web import models
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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
def login_new(request):
    if (request.method == "GET"):
        return render(request, "login.html")
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            # if username == 'admin' and password == 'admin123':
            # return HttpResponse("Login Success!")
            # return HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user', username, 3600) # 添加浏览器Cookie
            request.session['user'] = username  # 将session信息添加到浏览器
            response = HttpResponseRedirect('/dep_list')
            response.set_cookie('user', username, 3600)
            return response
        else:
            return render(request, 'login.html', {'error': 'username or password error'})
@login_required
def dep_list(request):
     #print(models.Department)
     all_dept=models.Department.objects.all()

     return render(request,"dep_list.html",{"all_depts":all_dept})
@login_required
def query_dep(request):
    dep_name=request.GET.get("dep_name")
    dep=models.Department.objects.filter(Q(dep_name=dep_name))
    return render(request,"dep_list.html",{"all_depts":dep})
@login_required
def dep_add(request):

        if request.method == "GET":
           return render(request,"dep_add.html")
        elif request.method == "POST":
            dep_name = request.POST.get("dep_name")
            models.Department.objects.create(dep_name=dep_name)
            return redirect("http://127.0.0.1:8000/dep_list/")
@login_required
def dep_del(request):
    del_id=request.GET.get("del_id")
    models.Department.objects.filter(id=del_id).delete()
    return  redirect("/dep_list/")
@login_required
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
@login_required
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
def hello(request):
    return render(request,"hello.html")
def my_view(request):
    my_objects = models.Department.objects.all()
    paginator = Paginator(my_objects, 2) # 分页，每页显示25条数据
    page = request.GET.get('page')
    my_objects = paginator.get_page(page) # 获取指定页数的数据
    return render(request, 'page.html', {'my_objects': my_objects})
@login_required
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


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from em_web.models import detection_collect
import json
@csrf_exempt
def get_search(request):
    search_list = []
    type = detection_collect.objects.values_list('type', flat=True)
    type_list = list(type)
    type_set = set(type_list)
    try:
        for i in type_set:
            count = type_list.count(i)
           # print(type(count))
            # print("the %s has found %d" %(i,type_list.count(i)))
            tem = {}
            tem['name'] = i
            tem['value'] = count
            search_list.append(tem)
        print('search_list:---', json.dumps(search_list))
    except Exception as e:
        print('e:', e)
     #HttpResponse(json.dumps(search_list), content_type='application/json')
    #search=json.dumps(search_list)
    #print('search:---', search)
    print(search_list[0]["name"])
    #print(type(search_list[0]["name"]))
    return render(request,"echart_test.html",{"search":search_list})
def Basic_Line_Chart(request):

# 查询出Person对象信息，也就是数据表中的所有数据
    # 一行数据就是一个对象，一个格子的数据就是一个对象的一个属性值
    objs = models.Person.objects.all()
    # locals函数可以将该函数中出现过的所有变量传入到展示页面中，即index.html文件中
  #  return render(request,'index.html',locals())
    return render(request,"Basic Line Chart.html",{"objs":objs})
def line_stack(request):
    return render(request,"line-stack.html")
def index(request):
    return render(request, "login.html")
