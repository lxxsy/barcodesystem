from django.shortcuts import render, redirect
from bc_formula.models import *
from django.core import serializers
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse
from .models import *
import re
import os


def product_save(request):
    if request.method == 'POST':
        proof = request.POST.get('proof')
        cpid = request.POST.get('cpid')
        cpmc = request.POST.get('cpmc')
        gg = request.POST.get('gg')
        dbz = request.POST.get('dbz')
        pw = request.POST.get('pw')
        bz = request.POST.get('bz')
        pbbh = request.POST.get('pbbh')
        cpxkz = request.POST.get('cpxkz')
        cpsx = request.POST.get('cpsx')
        cpxx = request.POST.get('cpxx')
        zbq = request.POST.get('zbq')
        cctj = request.POST.get('cctj')
        cpsb = request.POST.get('cpsb')
        cppic = request.POST.get('cppic')
        cpsm = request.FILES.get('cpsm')
        tempname = request.FILES.get('tempname')
        pattern = re.compile(r'\.+')
        cpsm_name_list = cpsm.name.split('.')
        cpsm_size = cpsm.size
        tempname_list = tempname.name.split('.')
        tempname_size = tempname.size
        if (cpid == '' or cpmc == '' or pbbh == '' or gg == '' or cpsm == '' or tempname == '' or
                cppic == '' or pattern.search(cpsx) or pattern.search(cpxx) or pattern.search(zbq) or
                cpsm_size > 5000000 or tempname_size > 5000000):
            return render(request, 'bc_product/product.html')
        cpsm_name_type = cpsm_name_list[len(cpsm_name_list) - 1]
        if cpsm_name_type != 'html' and cpsm_name_type != 'htm' and cpsm_name_type != 'dot':
            return render(request, 'bc_product/product.html')
        tempname_list_type = tempname_list[len(tempname_list)-1]
        if tempname_list_type != 'html' and tempname_list_type != 'htm' and tempname_list_type != 'dot':
            return render(request, 'bc_product/product.html')
        if not cpsx.isdigit():
            cpsx = None
        if not cpxx.isdigit():
            cpxx = None
        if not zbq.isdigit():
            zbq = None
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
    else:
        return render(request, 'bc_product/product.html')


def product_query(request, num):
    if num == 1:
        pb_list = serializers.serialize('json', Pb.objects.all())
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


def product_update(request):
    cpid = request.GET.get('cpid')
    cpml = Cpml.objects.get(cpid=cpid)
    context = {
        'cpid': cpml.cpid, 'cpmc': cpml.cpmc, 'gg': cpml.gg, 'cpxkz': cpml.cpxkz, 'pw': cpml.pw, 'bz': cpml.bz,
        'pbbh': cpml.pbbh, 'cpsx': cpml.cpsx, 'cpxx': cpml.cpxx, 'dbz': cpml.dbz, 'tempname': cpml.tempname,
        'zbq': cpml.zbq, 'cctj': cpml.cctj, 'cpsm': cpml.cpsm, 'cppic': cpml.cppic,
        'cpsb': cpml.cpsb, 'title': '修改产品', 'explain': '修改产品'
    }
    return render(request, 'bc_product/product.html', context)


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