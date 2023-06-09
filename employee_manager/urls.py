"""employee_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from em_web import views
from em_web.views import my_NewView
app_name='em_web'
urlpatterns = [
    path('admin/', admin.site.urls),
    path("dep_list/",views.dep_list),
    path("dep_add/",views.dep_add),
    path("dep_del/",views.dep_del),
    path("dep_update/",views.dep_update),
    path("emp_list/",views.emp_list),
    path("emp_del/",views.emp_del),
    path("emp_add/",views.emp_add),
    path("emp_update/",views.emp_update),
    path("query_dep/",views.query_dep),
    path("login/",views.login),
    path("china/",views.china),
    path("world/",views.world),
    path("page/",views.my_view),
    path("my_NewView/",views.my_NewView),
    path("my_NewView/<int:page>",views.my_NewView),
    path('my_NewView/<int:page>/<int:page_size>/', views.my_NewView),
    path('my-view/', my_NewView, name='my_NewView'),
    path('my-view/<int:page>/', my_NewView, name='my_NewView'),
    path('my-view/<int:page>/<int:page_size>/', my_NewView, name='my_NewView'),
    path("detection/",views.get_search),
    path("hello/",views.hello),
    path("Basic_Line_Chart/",views.Basic_Line_Chart),
    path("line_stack/",views.line_stack),
    path('accounts/login/', views.index),
    path("index/", views.index),
    path("login_new/", views.login_new),
    path("logout/",views.logout),
    path("dep_search/",views.dep_search),
    path("emp_list_search/",views.emp_list_search),
    path("department_list/",views.department_list),
    path("dep_list_ajax/",views.dep_list_ajax),
    path("department/<int:department_id>/delete/",views.delete_department),
    path('dep_list_ajax/department/<int:department_id>/delete/', views.delete_department),
    #path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('delete_department/', views.delete_department1, name='delete_department'),
    path("login1/",views.login1),
    re_path('^ajax/', views.ajax_test),
    re_path('^pro/', views.product),
    path("index_new/",views.index_new),
    path("index_json/",views.index_json),
    path('login_new_ajax/', views.login_new_ajax),
    path("layer_test/",views.layer),
    path("image/code/",views.image_code),
    path("login_index/",views.login_index),
    path("layerTest/",views.layerTest),
    path("formTest/",views.formTest),
    path("submit/",views.sumbit),
    path("User_list/",views.user_list),
    path("boot_demo/",views.boot_demo),
    path("my_view_redis/",views.my_view_redis),
    path('download/', views.download_file),
    path("download_employees/",views.download_employees),
    path("upload_file/",views.upload_file),
    path("import/",views.import_file),
    path("test/",views.test),
    path("download_dep/",views.download_dep_file),
    path("download_departments/",views.download_departments),
    path("upload_department_file/",views.upload_department_file),
    path("case_list/",views.case_list),
    path("api/",views.api),
]









