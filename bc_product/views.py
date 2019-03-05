from django.shortcuts import render, redirect
from bc_formula.models import *
from django.core import serializers
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse
from django.db import connection
from .models import *
import re
import os


def query_product(request, num):
    if num == 1:
        pb_list = serializers.serialize('json', Pb.objects.filter(validity=False))
        return JsonResponse({'pb_list': pb_list})
    elif num == 2:
        cpid = request.GET.get('cpid')
        original = request.GET.get('Original')
        bool = 1
        if cpid == original:
            return JsonResponse({'bool': bool})
        cpml = Cpml.objects.filter(cpid=cpid)
        if cpml:
            bool = 0
        return JsonResponse({'bool': bool})
    elif num == 3:
        cpmc = request.GET.get('cpmc')
        original = request.GET.get('Original')
        bool = 1
        if cpmc == original:
            return JsonResponse({'bool': bool})
        cpml = Cpml.objects.filter(cpmc=cpmc)
        if cpml:
            bool = 0
        return JsonResponse({'bool': bool})
    elif num == 4:
        pbbh = request.GET.get('pbbh')
        pb_list = Pb.objects.filter(pbbh=pbbh)
        pb_bool = 0
        pbname = ''
        if pb_list:
            if pb_list[0].validity is False:
                pb_bool = 1
            else:
                pb_bool = 2
            pbname = pb_list[0].pbname
        return JsonResponse({'pb_bool': pb_bool, 'pbname': pbname})
    elif num == 5:
        pbname = request.GET.get('pbname')
        pb_list = Pb.objects.filter(pbname=pbname)
        pb_bool = 0
        pbbh = ''
        if pb_list:
            if pb_list[0].validity is False:
                pb_bool = 1
            else:
                pb_bool = 2
            pbbh = pb_list[0].pbbh
        return JsonResponse({'pb_bool': pb_bool, 'pbbh': pbbh})


def update_product(request):
    cpid = request.GET.get('cpid')
    cpml = Cpml.objects.get(cpid=cpid)
    context = {
        'cpid': cpml.cpid, 'cpmc': cpml.cpmc, 'gg': cpml.gg, 'cpxkz': cpml.cpxkz, 'pw': cpml.pw, 'bz': cpml.bz,
        'pbbh': cpml.pbbh, 'cpsx': cpml.cpsx, 'cpxx': cpml.cpxx, 'dbz': cpml.dbz, 'tempname': cpml.tempname,
        'zbq': cpml.zbq, 'cctj': cpml.cctj, 'cpsm': cpml.cpsm, 'cppic': cpml.cppic,
        'cpsb': cpml.cpsb, 'title': '修改产品', 'explain': '修改产品'
    }
    return render(request, 'bc_product/product.html', context)


def save_product(request):
    if request.method == 'POST':
        proof = request.POST.get('proof')
        cpid = request.POST.get('cpid')
        cpmc = request.POST.get('cpmc')
        gg = request.POST.get('gg')
        dbz = request.POST.get('dbz')
        pw = request.POST.get('pw')
        bzbh = request.POST.get('bzbh')
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
        user_id = request.user.id
        print('**********************')
        print(user_id)
        print('************')
        if cpid == '' or cpmc == '' or pbbh == '' or pbname == '' or tempname is None:
            return redirect('/admin/bc_product/cpml/add/')
        pb.objects.filter(pbbhss)
        if cppic is not None:
            if cppic.size > 5000000:
                return redirect('/admin/bc_product/cpml/add/')
        if cpsm is not None:
            if cpsm.size > 5000000:
                return redirect('/admin/bc_product/cpml/add/')
        if tempname is not None:
            if tempname.size > 5000000:
                return redirect('/admin/bc_product/cpml/add/')
        judge_tuples = (dbz, cpsx, cpxx)
        logic_object = LogicProcessing()
        judge_result = logic_object.float_handle(judge_tuples)
        if judge_result == 'error':
            return redirect('/admin/bc_product/cpml/add/')
        if dbz == '':
            dbz = None
        if cpsx == '':
            cpsx = None
        if cpxx == '':
            cpxx = None
        if not zbq.isdigit():
            zbq = None
        cursor = connection.cursor()
        if not proof:
            try:
                Cpml.objects.create(cpid=cpid, cpmc=cpmc, gg=gg, dbz=dbz, pw=pw, cpxkz=cpxkz, cpsx=cpsx, cpxx=cpxx,
                                    zbq=zbq, cctj=cctj, cpsb=cpsb, cppic=cppic, cpsm=cpsm, tempname=tempname,
                                    pbbh_id=pbbh, bzbh=bzbh, user_id=user_id)
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_product/cpml/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_product/cpml/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_product/cpml/' + cpid + '/update/')
                '''
                print('6')
                cursor.callproc('cpml_I', (cpid, cpmc, gg, dbz, pw, cpxkz, cpsx, cpxx, zbq, cctj, cpsb,
                                             cppic, cpsm, tempname.name, pbbh, bzbh))
                print('7')
                connection.commit()
                cursor.close()
                connection.close()
                print('8')
                if addanother is None and add_edit is None:
                    print('9')
                    return redirect('/admin/bc_product/cpml/')
                elif addanother is not None and add_edit is None:
                    print('10')
                    return redirect('/admin/bc_product/cpml/add/')
                elif addanother is None and add_edit is not None:
                    print('11')
                    return redirect('/admin/bc_product/cpml/' + cpid + '/update/')
                '''
            except Exception as e:
                print(e)
                cursor.close()
                connection.close()
                return redirect('/admin/bc_product/cpml/add/')
        else:
            try:
                cursor.callproc('cpml_U', (cpid, cpmc, gg, dbz, pw, cpxkz, cpsx, cpxx, zbq, cctj, cpsb,
                                             cppic, cpsm, tempname, pbbh, bzbh, proof))
                connection.commit()
                cursor.close()
                connection.close()
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_product/cpml/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_product/cpml/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_product/cpml/' + cpid + '/update/')
            except Exception as e:
                print(e)
                cursor.close()
                connection.close()
                return redirect('/admin/bc_product/cpml/add/')
        '''
        if not proof:
            Cpml.objects.create(cpid=cpid, cpmc=cpmc, gg=gg, dbz=dbz, cpxkz=cpxkz, pw=pw, bz=bz, pbbh_id=pbbh, cpsx=cpsx,
                                cpxx=cpxx, tempname=tempname, zbq=zbq, cctj=cctj, cpsm=cpsm, cppic=cppic, cpsb=cpsb)
            return redirect('/admin/bc_product/cpml/')
        else:
            cpml = Cpml.objects.get(cpid=proof)
            cpml_list = cpml.cpsm.name.split('/')
            cpml_list[len(cpml_list)-1] = cpsm
            cpsm_g = '/'.join(cpml_list)
            print(cpml.cpsm)
            print(cpml.cpsm.name)
            print(type(cpml.cpsm.name))
            print('***************************************')
            print(cpsm_g)
            print('----------------------------------------------')
            Cpml.objects.filter(cpid=proof).update(cpid=cpid, cpmc=cpmc, gg=gg, dbz=dbz, cpxkz=cpxkz, pw=pw, bz=bz,
                                                   pbbh_id=pbbh, cpsx=cpsx, cpxx=cpxx, tempname=tempname,
                                                   zbq=zbq, cctj=cctj, cpsm=cpsm, cppic=cppic, cpsb=cpsb)
            return redirect('/admin/bc_product/cpml/')
        '''


def a(request):
    cpml = Cpml.objects.get(cpid='CP102')
    a = cpml.cpsm
    print(a.name)
    # q = []
    f = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
    #with open(os.path.join(f, a.name)) as f:
        #ff = f.read()
    #fff = ff.split('\n')
    #for i in fff:
    #    print(q.append(i.split('：')))
    print('111111111111111111111111')
    #qq = dict(q)
    context = {
        'cpmc': cpml.cpmc, 'ff': a
    }
    return render(request, 'bc_product/ceshi.html', context)


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



