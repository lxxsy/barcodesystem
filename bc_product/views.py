from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse, HttpResponse, Http404
from django.db import connection, transaction
from bc_production.models import Scjhb
from bc_formula.models import *
from .models import *
import re
import os

# C:\Users\44393\python\BarcodeSystem
BASE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def query_product(request, num):
    if num == 1:
        pb_list = serializers.serialize('json', Pb.objects.filter(validity=False))
        return JsonResponse({'pb_list': pb_list})
    elif num == 2:
        cpid = request.GET.get('cpid')
        original_cpid = request.GET.get('Original_cpid')
        bool_product = 1
        # 若新值与原值相同，说明未作修改，bool_gys=1返回True，正确
        if not cpid == original_cpid:
            # 两值不同则对新值进行查询，返回True说明已有此数据，不能修改返回False，错误
            if Cpml.objects.filter(cpid=cpid).exists():
                bool_product = 0
        return JsonResponse({'bool_product': bool_product})
    elif num == 3:
        cpmc = request.GET.get('cpmc')
        original_cpmc = request.GET.get('Original_cpmc')
        bool_product = 1
        # 若新值与原值相同，说明未作修改，bool_gys=1返回True，正确
        if not cpmc == original_cpmc:
            # 两值不同则对新值进行查询，返回True说明已有此数据，不能修改返回False，错误
            if Cpml.objects.filter(cpmc=cpmc).exists():
                bool_product = 0
        return JsonResponse({'bool_product': bool_product})
    elif num == 4:
        pbbh = request.GET.get('pbbh')
        original_pbbh = request.GET.get('Original_pbbh')
        pb_bool = 0
        pbname = ''
        pb_list = Pb.objects.filter(pbbh=pbbh)
        if pb_list.exists():
            pbname = pb_list[0].pbname
            if not pbbh == original_pbbh:
                if pb_list[0].validity is True:
                    pb_bool = 2
                else:
                    pb_bool = 1
            else:
                pb_bool = 1
        return JsonResponse({'pb_bool': pb_bool, 'pbname': pbname})
    elif num == 5:
        pbname = request.GET.get('pbname')
        original_pbname = request.GET.get('Original_pbname')
        pb_bool = 0
        pbbh = ''
        pb_list = Pb.objects.filter(pbname=pbname)
        if pb_list.exists():
            pbbh = pb_list[0].pbbh
            if not pbname == original_pbname:
                if pb_list[0].validity is True:
                    pb_bool = 2
                else:
                    pb_bool = 1
            else:
                pb_bool = 1
        return JsonResponse({'pb_bool': pb_bool, 'pbbh': pbbh})
    # 点击删除按钮时，会到此进行逻辑处理，把相关的文件从服务器删除掉
    elif num == 6:
        cpid = request.GET.get('cpid')
        try:
            cpml = Cpml.objects.get(cpid=cpid)
            cppic = cpml.cppic
            cpsm = cpml.cpsm
            tempname = cpml.tempname
            with transaction.atomic():
                # 此变量为用户id/文档类型/文档名字--数据库存储的路径,需要把/转换为\
                user_type_cppic_str = str(cppic).replace('/', '\\')
                if user_type_cppic_str != '':
                    # 源文档的绝对路径
                    root_path = os.path.join(BASE_ROOT, 'static\media', user_type_cppic_str)
                    os.remove(root_path)
                user_type_cpsm_str = str(cpsm).replace('/', '\\')
                if user_type_cpsm_str != '':
                    # 源文档的绝对路径
                    root_path = os.path.join(BASE_ROOT, 'static\media', user_type_cpsm_str)
                    # 删除源文档
                    os.remove(root_path)
                user_type_tempname_str = str(tempname).replace('/', '\\')
                if user_type_tempname_str != '':
                    # 源文档的绝对路径
                    root_path = os.path.join(BASE_ROOT, 'static\media', user_type_tempname_str)
                    # 删除源文档
                    os.remove(root_path)
                pb = Pb.objects.get(pbbh=cpml.pbbh_id)
                pb.validity = False
                pb.save()
                cpml.delete()
        except Exception as e:
            print(e)
            raise Http404('异常')
        return redirect('/admin/bc_product/cpml/')


def update_product(request):
    product_id = request.GET.get('product_id')
    bool_product = 1
    # 查询产品表是否有此产品代码，出现异常则进入except环节
    try:
        cpml = Cpml.objects.get(cpid=product_id)
        cppic = str(cpml.cppic)
        cpsm = str(cpml.cpsm)
        tempname = str(cpml.tempname)
        pbname = cpml.pbbh.pbname
        dbz = cpml.dbz
        cpsx = cpml.cpsx
        cpxx = cpml.cpxx
        zbq = cpml.zbq
        if dbz is None:
            dbz = ''
        if cpsx is None:
            cpsx = ''
        if cpxx is None:
            cpxx = ''
        if zbq is None:
            zbq = ''
        return JsonResponse({'bool_product': bool_product, 'cpid': cpml.cpid, 'cpmc': cpml.cpmc, 'gg': cpml.gg,
                             'dbz': dbz, 'pw': cpml.pw, 'cpxkz': cpml.cpxkz, 'cpsx': cpsx, 'cpxx': cpxx,
                             'zbq': zbq, 'cctj': cpml.cctj, 'cpsb': cpml.cpsb, 'cppic': cppic, 'cpsm': cpsm,
                             'tempname': tempname, 'pbbh': cpml.pbbh_id, 'pbname': pbname, 'bz': cpml.bz})
    # 出现错误，讲错误返回到前端
    except Exception as e:
        print(e)
        return JsonResponse({'bool_product': 'error'})


def save_product(request):
    if request.method == 'POST':
        proof = request.POST.get('proof')
        cpid = request.POST.get('cpid')
        cpmc = request.POST.get('cpmc')
        gg = request.POST.get('gg')
        dbz = request.POST.get('dbz')
        pw = request.POST.get('pw')
        bz = request.POST.get('bz')
        pbbh = request.POST.get('data_cpml_pbbh')
        pbname = request.POST.get('data_cpml_pbname')
        cpsx = request.POST.get('cpsx')
        cpxx = request.POST.get('cpxx')
        zbq = request.POST.get('zbq')
        cctj = request.POST.get('cctj')
        cpsb = request.POST.get('cpsb')
        cpxkz = request.POST.get('cpxkz')
        cppic = request.FILES.get('cppic')
        cpsm = request.FILES.get('cpsm')
        tempname = request.FILES.get('tempname')
        addanother = request.POST.get('_addanother')
        add_edit = request.POST.get('_continue')
        user_id = request.user.id  # 此方法可获取当前登陆操作用户的ID，此次在这里使用的目的是保存文件时用来区分文件夹，文件夹的分类采用一个用户一个文件夹
        if cpid == '' or cpmc == '' or pbbh == '' or pbname == '':
            return redirect('/admin/bc_product/cpml/add/')
        if cppic is not None:
            if cppic.size > 5000000:
                return redirect('/admin/bc_product/cpml/add/')
        if cpsm is not None:
            if cpsm.size > 5000000:
                return redirect('/admin/bc_product/cpml/add/')
        if tempname is not None:
            if tempname.size > 5000000:
                return redirect('/admin/bc_product/cpml/add/')
        # 将浮点数值统一打包成一个元组进行统一判断
        judge_tuples = (dbz, cpsx, cpxx)
        # 调用业务逻辑处理类，获得一个实例
        logic_object = LogicProcessing()
        # 调用浮点数处理方法，将元组参数传递过去
        judge_result = logic_object.float_handle(judge_tuples)
        # 结果值为error，则重定向
        if judge_result == 'error':
            return redirect('/admin/bc_product/cpml/add/')
        # 为空全部转为None，因为数据表中得类型为整型与浮点型，存放空字符串是不行得
        if dbz == '':
            dbz = None
        if cpsx == '':
            cpsx = None
        if cpxx == '':
            cpxx = None
        if not zbq.isdigit():
            zbq = None
        # 连接数据库，得到一个游标，因为此视图不使用存储过程，所以此游标没有使用
        # cursor = connection.cursor()
        if not proof:
            try:
                if tempname is None:
                    return redirect('/admin/bc_product/cpml/add/')
                # 查看Pb表是否有此配方编号并且v值是F，不是F则说明此配方已经有产品使用，如果达不到这两种条件则重定向
                if not Pb.objects.filter(pbbh=pbbh, validity=False).exists():
                    return redirect('/admin/bc_product/cpml/add/')
                # 开启事务atomic上下文管理器，with块内的处理会纳入事务管理，有错误则全部回滚
                with transaction.atomic():
                    Cpml.objects.create(cpid=cpid, cpmc=cpmc, gg=gg, dbz=dbz, pw=pw, cpxkz=cpxkz, cpsx=cpsx, cpxx=cpxx,
                                        zbq=zbq, cctj=cctj, cpsb=cpsb, cppic=cppic, cpsm=cpsm, tempname=tempname,
                                        pbbh_id=pbbh, bz=bz, user_id=user_id)
                    # 新增成功后，将此配方编号的v值改为T，这样在新增产品时会自动排除此配方，因为一个配方只能有一个产品
                    pb_source_row = Pb.objects.get(pbbh=pbbh)
                    pb_source_row.validity = True
                    pb_source_row.save()
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_product/cpml/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_product/cpml/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_product/cpml/' + cpid + '/update/')
            except Exception as e:
                print(e)
                return redirect('/admin/bc_product/cpml/add/')
        else:
            try:
                # 获取修改之前的数据，将之前的文档删除掉，在添加新的文档
                cpml_source_row = Cpml.objects.get(cpid=proof)
                new_cppic = cpml_source_row.cppic
                new_cpsm = cpml_source_row.cpsm
                new_tempname = cpml_source_row.tempname
                # 开启事务atomic上下文管理器，with块内的处理会纳入事务管理，有错误则全部回滚
                with transaction.atomic():
                    # 判断是否为空，下方逻辑处理全部相同
                    if cppic is not None:
                        # 不为空去文件处理方法进行逻辑处理，返回的值可以直接放入数据库中
                        new_cppic = logic_object.file_handle(new_cppic, user_id, cppic)
                    if cpsm is not None:
                        new_cpsm = logic_object.file_handle(new_cpsm, user_id, cpsm)
                    if tempname is not None:
                        new_tempname = logic_object.file_handle(new_tempname, user_id, tempname)
                    pb_source_row = Pb.objects.get(pbbh=cpml_source_row.pbbh_id)
                    pb_source_row.validity = False
                    pb_source_row.save()
                    Cpml.objects.filter(cpid=proof).update(cpid=cpid, cpmc=cpmc, gg=gg, dbz=dbz, pw=pw, cpxkz=cpxkz,
                                                           cpsx=cpsx, cpxx=cpxx, zbq=zbq, cctj=cctj, cpsb=cpsb,
                                                           cppic=new_cppic, cpsm=new_cpsm, tempname=new_tempname,
                                                           pbbh_id=pbbh, bz=bz, user_id=user_id)
                    pb_new_row = Pb.objects.get(pbbh=pbbh)
                    pb_new_row.validity = True
                    pb_new_row.save()
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_product/cpml/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_product/cpml/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_product/cpml/' + cpid + '/update/')
            except Exception as e:
                print(e)
                return redirect('/admin/bc_product/cpml/add/')


def quality_trace_back(request):
    spl = request.GET.get('SPL')
    scjhb = Scjhb.objects.get(spl=spl)
    cpid = scjhb.cpid_id
    cpml = Cpml.objects.get(cpid=cpid)
    cppic_url = str(cpml.cppic)
    cpsm_url = str(cpml.cpsm)
    content = {
        'spl': scjhb.spl, 'scrq': scjhb.scrq, 'cpname': cpml.cpmc, 'cppic': cppic_url, 'cpsm': cpsm_url
    }
    return render(request, 'bc_product/quality_trace_back.html', content)


class LogicProcessing(object):
    '''业务逻辑处理'''
    # 初始化对象，判断值属性初始化为'error'
    def __init__(self):
        self.judge_value = 'error'
        self.pattern_one = re.compile(r'^[1-9][0-9]?$')
        self.pattern_two = re.compile(r'^[0-9]+\.?[0-9]*$')
        self.pattern_three = re.compile(r'^0+\.?0*$')

    # 浮点数处理方法
    def float_handle(self, judge_value):
        # 参数类型为str时执行if
        if type(judge_value) is str:
            # 值为空则赋值None
            if judge_value == '':
                self.judge_value = None
                return self.judge_value
            else:
                # 否则判断是否为数字，不是数字则为默认值'error'
                if self.pattern_two.match(judge_value):
                    # 是数字则判断是否为不合理数字，不是则赋值原值，不合理数字为:00，0.0等以0开头的数字
                    if not self.pattern_three.match(judge_value):
                        self.judge_value = judge_value
            return self.judge_value
        # 参数类型为列表或元组时执行elif
        elif type(judge_value) is list or type(judge_value) is tuple:
            for sequence_value in judge_value:
                if sequence_value == '':
                    self.judge_value = None
                else:
                    if self.pattern_two.match(sequence_value):
                        if self.pattern_three.match(sequence_value):
                            self.judge_value = 'error'
                            break
                        else:
                            self.judge_value = None
                    else:
                        self.judge_value = 'error'
                        break
            return self.judge_value

    # 文件处理方法
    def file_handle(self, new_file, user_id, file):
        # 判断新文件后缀，进行分类
        ext = file.name.split('.')[-1]
        sub_folder = 'grf'
        if ext.lower() in ["jpg", "png", "gif"]:
            sub_folder = "picture"
        elif ext.lower() not in ["grf"]:
            sub_folder = "document"
        try:
            # 判断从数据库读取到的数据是否为空字符，此数据需要手动转换为字符类型。
            # 为空表示没有文件，不需要进行删除文件操作
            if str(new_file) != '':
                # 此变量为用户id/文档类型/文档名字--数据库存储的路径,需要把/转换为\
                user_type_file_str = str(new_file).replace('/', '\\')
                # 源文档的绝对路径
                root_path = os.path.join(BASE_ROOT, 'static\media', user_type_file_str)
                if os.path.exists(root_path):
                    # 删除源文档
                    os.remove(root_path)
            # 新文档数据库存储路径
            sql_path = os.path.join(str(user_id), sub_folder, file.name)
            # 创建新文件，名字就叫做文档的名字
            file_path = os.path.join(BASE_ROOT, 'static\media', sql_path)
            # 打开这个新创建的新文件，并写入数据
            f = open(file_path, 'wb')
            for chunk in file.chunks():
                f.write(chunk)
        except Exception as e:
            print(e)
        else:
            # 将新文档存储路径的\转换为/
            new_file = sql_path.replace('\\', '/')
            return new_file


