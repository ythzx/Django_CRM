from django.shortcuts import render, HttpResponse, redirect
from Django_admin import models
from django.forms import Form, ModelForm
from django.forms import fields as ffields
from django.forms import widgets as fwidgets


class TestModelFrom(ModelForm):
    # 单独定制字段的,# 这个的优先级高于下面的labels,
    # 这里的名字要和数据库的字段名一致
    user = ffields.CharField(label='用户名', error_messages={'required': "用户名不能为空"})
    email = ffields.EmailField(label='邮箱', error_messages={'required': "邮箱不能为空", 'invalid': "邮箱格式错误"})

    # m2m = ffields.CharField(label='角色', error_messages={'required': "角色不能为空"})

    class Meta:
        model = models.UserInfo  # 对应表的model
        fields = "__all__"  # 显示所有的字段 也可用元组定制自己的字段 ('user','email')

        """
        # 错误信息 验证未通过，前端显示错误信息
        error_messages = {
            'user':{'required':"用户名不能为空"},
            'email':{'required':"邮箱不能为空",'invalid':"邮箱格式错误"}
        }
        # labels是把前端使用form.as_p 生成标签的时候 把字段名转换成中文
        labels = {
            'user':"用户名",
            'email':"邮箱",
            'ug':"用户组",
            'm2m':"角色"
        }
        # help_texts = {
        #     'user':"请输入用户名"
        # }
        """


def test(request):
    """
    添加新的用户信息
    :param request:
    :return:
    """
    if request.method == "GET":
        form = TestModelFrom()  # 测试可知form对象中是生成的标签
        context = {
            'form': form
        }
        # {'form': <TestModelFrom bound=False, valid=False, fields=(user;email;ug;m2m)>}
        # 转换成字典直接发送到前端，字典中包含form对象，数据库的字段等
        return render(request, 'test.html', context)
    else:
        form = TestModelFrom(request.POST)  # 需要传入request参数
        if form.is_valid():
            form.save()  # 通过form对象直接保存
        context = {
            'form': form
        }
        return render(request, 'test.html', context)


def edit(request, nid):
    """
    用户编辑
    :param request:
    :param nid: 前端传过来的参数，
    :return:
    """
    obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = TestModelFrom(instance=obj)  # 修改的时候参数是instance
        context = {
            'form': form
        }
        return render(request, 'edit.html', context)
    else:
        """
        TestModelForm 继承了BaseModelForm 里面的参数，instance代表修改
        data 代表全部的数据，files代表文件数据
        """
        form = TestModelFrom(instance=obj, data=request.POST, files=request.FILES)
        context = {
            'form': form
        }
        return render(request, 'edit.html', context)
