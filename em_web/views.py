import datetime
from datetime import datetime
from time import timezone

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import  messages
# from models import models
from em_web import models
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count
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
           # response=redirect("/dep_list/")
            #response.set_cookie('name', name,max_age=60)
            #return response
            return  HttpResponse("登录成功")
        messages.error(request, '用户名或密码错误！')
        return render(request, "login.html", {"error": "用户名或密码错误！"})
#@csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie
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
    search = request.GET.get("search")
    print(search)
    if search==None:
     #print(models.Department)
     #print(request.user.is_authenticated())
          all_dept=models.Department.objects.all().order_by("id")
          return render(request,"dep_list.html",{"all_depts":all_dept})
    else:
        all_dept = models.Department.objects.filter(dep_name__contains=search)
        return render(request, "dep_list.html", {"all_depts": all_dept,"search_data": search})
def department_list(request):
    search = request.GET.get("search")
    print(search)
    if search == None:
       departments = models.Department.objects.all()
       context = {'departments': departments}
       return render(request, 'dep_new_list.html', context)
    else:
        departments=models.Department.objects.filter(dep_name__contains=search)
        context = {'departments': departments,
                   "search_data": search}
        return render(request, 'dep_new_list.html', context)

def dep_search(request):
    search=request.GET.get("search")
    all_dept=models.Department.objects.filter(dep_name=search)
    return render(request, "dep_list.html", {"all_depts": all_dept,"search_data": search})
@login_required
def query_dep(request):
    dep_name=request.GET.get("dep_name")
    dep=models.Department.objects.filter(Q(dep_name=dep_name))
    return render(request,"dep_list.html",{"all_depts":dep})
@login_required
def dep_add(request):
        print(request.user.is_authenticated)
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
    #messages.success(request,' 已被成功删除！')
    return  redirect("/dep_list/")
@login_required
def emp_del(request):
    del_id=request.GET.get("del_id")
    models.Employee.objects.filter(id=del_id).delete()
    return redirect("/emp_list/")
@login_required
def emp_add(request):
    if request.method=="GET":
       emp_list = models.Employee.objects.all()
       gender=[]
       for emp in emp_list:
           emp_gender=emp.get_gender_display()
           print(emp_gender)
           gender.append(emp_gender)
       print(gender)
       print(emp_list.first().get_gender_display())
       departmnets=models.Department.objects.all()
       choices = models.Employee.gender_choices
       return render(request,"emp_add.html",{'choices': choices,"departments":departmnets})
    #elif request.method=="POST":
    if request.method == 'POST':
        name = request.POST.get('emp_name')
        password = request.POST.get('emp_password')
        age = request.POST.get('age')
        account = request.POST.get('account')
        create_time = request.POST.get('create_time')
        gender = request.POST.get('gender')
        dep_id = request.POST.get('department')
        models.Employee.objects.create(
            name=name,
            password=password,
            age=age,
            account=account,
            create_time=create_time,
            gender=gender,
            dep_id=dep_id
        )
        return redirect("/emp_list/")

@login_required
def dep_update(request):
    update_dep_id= None
    if request.method=="GET":
        update_dep_id=request.GET.get("update_id")
        default_dep= models.Department.objects.filter(id=update_dep_id).first()

        return render(request,"dep_update.html",{
            "default_dep":default_dep
        })
    if request.method =="POST":
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

    #all_emp_data=all_emp_data.order_by("age")

    return render(request,"emp_list.html",{"emp_queryset":all_emp_data})

def emp_list_search(request):
    search = request.GET.get("search")
    print(search)
    if search == None:
        # print(models.Department)
        # print(request.user.is_authenticated())
        all_emp_data = models.Employee.objects.all().order_by('-create_time')
        page_size = request.GET.get('per_page') or 10  # 默认每页显示2条
        paginator = Paginator(all_emp_data, page_size)
        page = request.GET.get('page')
        all_emp_data=paginator.get_page(page)
        for emp in all_emp_data:
            emp.create_time = emp.create_time.strftime("%Y-%m-%d")
            emp.gender = emp.get_gender_display()
            emp.dep_id = models.Department.objects.filter(id=emp.dep_id).first()
        return render(request, "emp_list.html", {"emp_queryset": all_emp_data, 'page_sizes': [2, 5, 10],}) # 定义可选的每页条数})
    else:
        all_emp_data = models.Employee.objects.filter(name__contains=search)
        page_size = request.GET.get('per_page') or 2  # 默认每页显示2条
        paginator = Paginator(all_emp_data, page_size)
        page = request.GET.get('page')
        all_emp_data = paginator.get_page(page)
        for emp in all_emp_data:
            emp.create_time = emp.create_time.strftime("%Y-%m-%d")
            emp.gender = emp.get_gender_display()
            emp.dep_id = models.Department.objects.filter(id=emp.dep_id).first()

        return render(request, "emp_list.html", {"emp_queryset": all_emp_data,"search":search,'page_sizes': [2, 5, 10]})
from django.utils import timezone
@login_required
def emp_update(request):
   # update_emp_id = None
    if request.method == "GET":
        update_emp_id = request.GET.get("update_id")
        #default_emp = models.Employee.objects.filter(id=update_emp_id).first()
       # print(default_emp)
      #  print(default_emp.id)
        employee = models.Employee.objects.get(id=update_emp_id)
        departments = models.Department.objects.all()
        #gender_choices = models.Employee.GENDER_CHOICES
        emp = models.Employee.objects.filter(id=update_emp_id).first()
        print(emp.dep_id)
        emp_dep_id=emp.dep_id
        gender = emp.get_gender_display()
        # 将 create_time 格式化为年月日格式，并转换为与前端页面相同时区的日期
        create_time = timezone.localtime(emp.create_time).strftime("%Y-%m-%d")
        create_time = timezone.localtime(emp.create_time).strftime("%Y-%m-%d")
        print(gender)
        gender_id=emp.gender
        print(gender_id)
        #departments = models.Department.objects.all()
        department = emp.dep
        print(department)
        gender_choices = models.Employee.gender_choices
        return render(request,"emp_update.html",{"default_emp_id":update_emp_id,"emp":emp,"emp_dep_id": emp_dep_id,"departments": departments, "gender_choices": gender_choices, "selected_dep": department, "selected_gender": gender,"gender_id":gender_id})
    if request.method=="POST":
        update_emp_id = request.POST.get("update_id")
       # emp = models.Employee.objects.filter(id=update_emp_id).first()
        print(update_emp_id)
        name = request.POST.get('emp_name')
        password = request.POST.get('emp_password')
        age = request.POST.get('age')
        account = request.POST.get('account')
        create_time = request.POST.get('create_time')
        gender = request.POST.get('gender')
       # gender_id=emp.gender
        dep_id = request.POST.get('department')
        models.Employee.objects.filter(id=update_emp_id).update( name=name,
            password=password,
            age=age,
            account=account,
            create_time=create_time,
            gender=gender,
            dep_id=dep_id)
        return redirect("/emp_list/")


def china(request):
    return render(request,"china.html")
def world(request):
    return render(request,"world.html")
def hello(request):
    return render(request,"hello.html")
def my_view(request):
    my_objects = models.Department.objects.all()
    paginator = Paginator(my_objects, 2) # 分页，每页显示2条数据
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


from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
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
    print(request.user.is_authenticated)
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
def logout(request):
    auth.logout(request)
    return redirect("/index")
from django.views.decorators.cache import cache_page
import redis

# 获取Redis连接
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
@cache_page(60 * 15)  # 缓存 15 分钟
def index(request):
    return render(request, "login.html")
def logout(request):
    auth.logout(request)
    return redirect("/index")
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Department
from django.http import JsonResponse

def delete_department(request, department_id):
    department = models.Department.objects.get(id=department_id)
    department.delete()
    return JsonResponse({'status': 'success'})
def dep_list_ajax(request):
    departments=models.Department.objects.all()
    return render(request,"dep_list_ajax.html",{"departments":departments})
def delete_department(request, department_id):
    # 首先找到要删除的部门对象
    department = get_object_or_404(Department, id=department_id)

    # 删除部门对象
    department.delete()

    # 返回响应
    return JsonResponse({'success': True})
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def delete_department1(request):
    # 获取前端发送来的部门 ID
    department_id = request.POST.get('department_id')
    # 根据部门 ID 获取 Department 对象
    department = get_object_or_404(Department, id=department_id)

    # 删除部门，注意这里使用 delete 方法实际删除记录
    department.delete()
    # 返回成功删除的状态信息
    return JsonResponse({'success': True})
import json
@csrf_exempt
def login1(request):

    if request.method == 'GET':
        return render(request,'ajax_text.html')
    else:
        uname = request.POST.get('uname')
        print(uname)
        pwd = request.POST.get('pwd')
        if uname == 'test' and pwd == '123':
            # return redirect('app03:show_book')
            ret = {'code':0,'success':'/app03/show_book/'}
            return HttpResponse(json.dumps(ret))
        else:
            # return redirect('app03:login')
            ret = {'code':1,'fail':'用户名或密码错误！！'}  #只需要改这里就行，提示一句话就行。
            return HttpResponse(json.dumps(ret))
def ajax_test(request):
    return render(request,'ajax.html')

def product(request):
    if request.method == "GET":
        a1 = request.GET.get('a1')
        a2 = request.GET.get('a2')
        a = int(a1)*int(a2)
        print(type(a))
        return HttpResponse(a)
def index_new(request):
    if request.method=="POST":
        i1=request.POST.get("i1")
        i2=request.POST.get("i2")
        i3=int(i1)+int(i2)
        return HttpResponse(i3)
    return render(request,"index.html")
@csrf_exempt
def index_json(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        i1 = float(data['i1'])
        i2 = float(data['i2'])
        result = i1 + i2
        return HttpResponse(result, content_type="application/json")
    return render(request, "index_new.html")
from django.http import HttpRequest
@csrf_exempt
def login_new_ajax(request):
    dic = {'status':None,'msg':None}  # 设置dic保存状态码及登入状态信息
    # 如果是ajax请求
    #if request.is_ajax():
    #if isinstance(request, HttpRequest) and request.is_ajax():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.POST.get('name')  # 获取用户名
        pwd = request.POST.get('pwd')    # 获取密码
        user_obj = models.LoginUser.objects.filter(name=name,pwd=pwd).first()  # 拿到对象
        if user_obj:
            dic['status'] = 200  # 存在状态码设置成200
        else:
            dic['status'] = 201
            dic['msg'] = '用户名或密码错误'

        # 方式一 : 直接使用JsonResponse
        return JsonResponse(dic)  # 将登入状态dic返回给前端ajax
        # 方式二 : 手动转json格式
        # import json
        # return HttpResponse(json.dumps(dic))
    return render(request,'login_new.html')  # get请求展示login页面
def layer(request):
    return render(request,"layer_text.html")
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
def check_code(width=120, height=30, char_length=4, font_file=r'C:\Users\admin\employee_manager\em_web\static\fonts\kumo.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)

from io import BytesIO

def image_code(request):

    ''' 生成图片验证码 '''
    img, code_string = check_code()
    # 写入到自己的session中（以便后续获取验证码在进行校验）
    request.session['image_code'] = code_string
    # 给session设置60s超时
    print(code_string)
    request.session.set_expiry(60)
    # print(code_string)
    stream = BytesIO()
    img.save(stream, 'png')
    #print(stream.getvalue())
    return HttpResponse(stream.getvalue())
@csrf_exempt
def login_index(request):
    if request.method=="GET":
       return render(request,"login_index.html")
    elif request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        verify_code=request.POST.get("code")
        print(verify_code)
        print(request.POST)
        code=request.session.get("image_code")
        if (username=="admin" and password=="123456" and verify_code==code):
            #return HttpResponse("登录成功！！！")
            return redirect("/boot_demo/")
        #return render(request,"login_index.html")
        return HttpResponse("用户名密码或验证码有误！！！")
def layerTest(request):
    return render(request,"layerTest.html")
def formTest(request):
    return render(request,"formTest.html")
from django.shortcuts import render
from em_web.models import User
@csrf_exempt
def sumbit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        user = User(name=name, email=email, age=age)
        user.save()
        Users=models.User.objects.all()
        #return HttpResponse("添加成功！")
       # return render(request,"User_list.html")
        return redirect("/User_list/")
    else:
        return render(request, 'formTest.html')
def user_list(request):
   # key = "my_key"
    #value = cache.get(key)
    Users = models.User.objects.all()
    return render(request,"User_list.html",{"Users":Users})
def boot_demo(request):
    return render(request,"boot_demo.html")
from django.core.cache import cache
import redis

# 在 Django 的 settings.py 中配置 Redis 的连接信息
redis_instance = redis.Redis(host='localhost', port=6379)

# 定义一个函数，将传递的键值对存储到 Redis 中
def set_key(request):
    key = request.GET.get('key')
    value = request.GET.get('value')
    if key and value:
        redis_instance.set(key, value)
        return HttpResponse('key value pair set successfully')
    else:
        return HttpResponse('key and value parameters required')

# 定义一个函数，从 Redis 中获取指定键的值
def get_key(request):
    key = request.GET.get('key')
    if key:
        value = redis_instance.get(key)
        if value:
            return HttpResponse(value)
        else:
            return HttpResponse('key does not exist')
    else:
        return HttpResponse('key parameter required')

# 在 Django views 中引用上述函数
def example_view(request):
    # 调用 set_key 函数将键值对存储到 Redis 中
    set_key(request)

    # 调用 get_key 函数从 Redis 获取指定键的值
    value = get_key(request)

    # 渲染模板并返回响应
    return render(request, 'example_template.html', {'value': value})
def my_view_redis(request):
    #cache.set('key1', 'Hello, Redis!')
    key = "my_key"
    value = cache.get(key)
    print(value)
    if value is None:
     value = models.User.objects.all()
      #print(value)
     cache.set(key, value,timeout=30)
    return render(request, "User.html", {"User_list": value})
from django.views.decorators.cache import cache_page
import redis

# 获取Redis连接
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)

@cache_page(60 * 15)  # 缓存 15 分钟
def my_view(request):
    # 视图函数的代码
    return HttpResponse('Hello, world!')
from django.http import FileResponse
import os

"""def download_file(request):
    # 获取要下载的文件的路径
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media/example.txt')
    # 打开文件并读取它的内容
    with open(file_path, mode='r', encoding='utf-8') as f:
        file_content = f.read()
    response = HttpResponse(file_content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="example.txt"'
    return response"""
def download_file(request):
    # 获取要下载的文件的路径
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media/employees.csv')
    # 打开文件并读取它的内容
    with open(file_path, mode='r', encoding='gbk') as f:
        file_content = f.read()
    response = HttpResponse(file_content, content_type='text/csv; charset=gbk')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    return response
import csv


def download_employees(request):
    employees = models.Employee.objects.all()
    print(employees[0].dep)
    print(type(employees[0].dep))

    # 将查询集的数据转换为 CSV 格式的文本数据
    response_text = '\ufeff' + '\n'.join([
        ','.join(["员工ID","员工姓名","员工密码","员工年龄","账户余额","入职时间","员工性别","所属部门"])  # CSV 表头
    ] + [
        ','.join([str(employee.id), employee.name, str(employee.password),str(employee.age),str(employee.account),(str(employee.create_time))[:10], str(employee.get_gender_display()),str(employee.dep)])  # CSV 行数据
        for employee in employees
    ])

    # 创建响应对象
    response = HttpResponse(response_text, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    return response


import csv
from io import TextIOWrapper
from datetime import datetime

from django.shortcuts import render
from .models import Employee

from datetime import datetime
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        csv_file = TextIOWrapper(request.FILES['file'].file, encoding=request.encoding)
        reader = csv.DictReader(csv_file)
        input_format = '%Y/%m/%d'
        output_format = '%Y-%m-%d'

        # 解析日期字符串并重新格式化日期
        old_date_str = '2023/1/2'
        old_date = datetime.strptime(old_date_str, input_format)
        new_date_str = datetime.strftime(old_date, output_format)
        from django.utils import timezone
        print(new_date_str)  # 输出：'2023-01-02'
        dep_list = models.Department.objects.all()
        deps = {}
        for dep in dep_list:
            # print(dep.dep_name)
            print({dep.dep_name: dep.id})
            deps[dep.dep_name] = dep.id
        print(deps)
        for row in reader:
            gender_dict = {'男': 1, '女': 2}
            gender = gender_dict.get(row['员工性别'])
            dep_id = deps.get(row['所属部门'])
            employee = Employee(
                id=row['员工ID'],  # 将CSV字段映射到模型的字段
                name=row['员工姓名'],
                password=row['员工密码'],
                age=row['员工年龄'],
                account=row['账户余额'],
                gender=gender,
                dep_id=dep_id,
                create_time=datetime.strptime(row['入职时间'],'%Y-%m-%d %H:%M:%S%z').date()  # 将字符串转换为日期
            )
            print(row['入职时间'])
           # print(Employee.dep)
            employee.save()

        return redirect("/emp_list_search/")
    return render(request, 'emp_list.html')
def import_file(request):
    return render(request,"import.html")
def test(request):
    dep_list=models.Department.objects.all()
    deps={}

    for dep in dep_list:
        #print(dep.dep_name)
        print({dep.dep_name:dep.id})
        deps[dep.dep_name]=dep.id
    print(deps)

    print(dep_list)
    return HttpResponse("jjjjj")
def download_dep_file(request):
    # 获取要下载的文件的路径
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media/departments.csv')
    # 打开文件并读取它的内容
    with open(file_path, mode='r', encoding='gbk') as f:
        file_content = f.read()
    response = HttpResponse(file_content, content_type='text/csv; charset=gbk')
    response['Content-Disposition'] = 'attachment; filename="department.csv"'
    return response
def download_departments(request):
    departments = models.Department.objects.all()
    # 将查询集的数据转换为 CSV 格式的文本数据
    response_text = '\ufeff' + '\n'.join([
        ','.join(["部门ID","部门名称","部门人数"])  # CSV 表头
    ] + [
        ','.join([str(department.id), str(department.dep_name), str(department.employee_count())])  # CSV 行数据
        for department in departments
    ])

    # 创建响应对象
    response = HttpResponse(response_text, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="departments.csv"'
    return response
def upload_department_file(request):
    if request.method == 'POST' and request.FILES['file']:
        csv_file = TextIOWrapper(request.FILES['file'].file, encoding=request.encoding)
        reader = csv.DictReader(csv_file)
        dep_list = models.Department.objects.all()
        for row in reader:
            departmrnt = Department(
                id=row['部门ID'],  # 将CSV字段映射到模型的字段
                dep_name=row['部门名称'],
            )
        departmrnt.save()
        return render(request, 'emp_list.html')
    return redirect("/emp_list_search/")

def case_list(request):
    cases=models.InterfaceCase.objects.all()
    return render(request,"case_list.html",{"cases":cases})