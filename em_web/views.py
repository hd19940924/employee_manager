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
        for emp in all_emp_data:
            emp.create_time = emp.create_time.strftime("%Y-%m-%d")
            emp.gender = emp.get_gender_display()
            emp.dep_id = models.Department.objects.filter(id=emp.dep_id).first()
        return render(request, "emp_list.html", {"emp_queryset": all_emp_data})
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