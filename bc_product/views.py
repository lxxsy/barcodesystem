from django.shortcuts import render, redirect
from bc_formula.models import *
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from .models import *
import re


def product_save(request):
    if request.method == 'POST':
        proof = request.POST.get('proof')
        cpid = request.POST.get('cpid')
        cpmc = request.POST.get('cpmc')
        bzgg = request.POST.get('bzgg')
        cpxkz = request.POST.get('cpxkz')
        pw = request.POST.get('pw')
        bz = request.POST.get('bz')
        pbbh = request.POST.get('pbbh')
        gg = request.POST.get('gg')
        cpsx = request.POST.get('cpsx')
        cpxx = request.POST.get('cpxx')
        zczbq = request.POST.get('zczbq')
        zjzbq = request.POST.get('zjzbq')
        cctj = request.POST.get('cctj')
        cpgg = request.POST.get('cpgg')
        cpsb = request.POST.get('cpsb')
        cpsm = request.FILES.get('cpsm')
        tempname = request.FILES.get('tempname')
        print('1111111111111111111111')
        print(cpsm)
        pattern = re.compile(r'\.+')
        cpsm_name_list = cpsm.name.split('.')
        cpsm_size = cpsm.size
        tempname_list = tempname.name.split('.')
        tempname_size = tempname.size
        if (cpid == '' or cpmc == '' or pbbh == '' or cpgg == '' or cpsm == '' or tempname == '' or
                pattern.search(cpsx) or pattern.search(cpxx) or pattern.search(zczbq) or pattern.search(zjzbq) or
                cpsm_size > 5000000 or tempname_size > 5000000):
            return render(request, 'bc_product/product.html')
        cpsm_name_type = cpsm_name_list[len(cpsm_name_list) - 1]
        if cpsm_name_type != 'doc' and cpsm_name_type != 'docx' and cpsm_name_type != 'eddx':
            return render(request, 'bc_product/product.html')
        tempname_list_type = tempname_list[len(tempname_list)-1]
        if tempname_list_type != 'doc' and tempname_list_type != 'docx' and tempname_list_type != 'eddx':
            return render(request, 'bc_product/product.html')
        if not cpsx.isdigit():
            cpsx = None
        if not cpxx.isdigit():
            cpxx = None
        if not zczbq.isdigit():
            zczbq = None
        if not zjzbq.isdigit():
            zjzbq = None
        if not proof:
            Cpml.objects.create(cpid=cpid, cpmc=cpmc, bzgg=bzgg, cpxkz=cpxkz, pw=pw, bz=bz, pbbh_id=pbbh, cpsx=cpsx,
                                cpxx=cpxx, gg=gg, tempname=tempname, zczbq=zczbq, zjzbq=zjzbq, cctj=cctj, cpsm=cpsm,
                                cpgg=cpgg, cpsb=cpsb)
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
            Cpml.objects.filter(cpid=proof).update(cpid=cpid, cpmc=cpmc, bzgg=bzgg, cpxkz=cpxkz, pw=pw, bz=bz,
                                                   pbbh_id=pbbh, cpsx=cpsx, cpxx=cpxx, gg=gg, tempname=tempname,
                                                   zczbq=zczbq, zjzbq=zjzbq, cctj=cctj, cpsm=cpsm_gs, cpgg=cpgg, cpsb=cpsb)
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
    print('--------------------------------------')
    print(cpml.cpsm)
    print('---------------------------------------')
    context = {
        'cpid': cpml.cpid, 'cpmc': cpml.cpmc, 'bzgg': cpml.bzgg, 'cpxkz': cpml.cpxkz, 'pw': cpml.pw, 'bz': cpml.bz,
        'pbbh': cpml.pbbh, 'cpsx': cpml.cpsx, 'cpxx': cpml.cpxx, 'gg': cpml.gg, 'tempname': cpml.tempname,
        'zczbq': cpml.zczbq, 'zjzbq': cpml.zjzbq, 'cctj': cpml.cctj, 'cpsm': cpml.cpsm, 'cpgg': cpml.cpgg,
        'cpsb': cpml.cpsb, 'title': '修改产品', 'explain': '修改产品'
    }
    return render(request, 'bc_product/product.html', context)