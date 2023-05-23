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
from django.urls import path
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

]
