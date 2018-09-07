from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from bc_product.models import *
from django.core import serializers, paginator
from django.db import transaction
from django.contrib.auth.models import User
import re


def select_product(request, num):
    '''
        接收ajax请求，查询数据并提交,num变化查询的数据会变化
    '''
    # 查询所有产品，序列化为json格式，不然传递不过去，不接收查询集
    if num == 1:
        cpml_list = serializers.serialize('json', Cpml.objects.all())
        return JsonResponse({'cpml_list': cpml_list})
    # 查询产品和配方的id与名字
    elif num == 2:
        cpid = request.GET.get('cpid')
        cpml = Cpml.objects.filter(cpid=cpid)
        if cpml:
            cpbh = cpml[0].cpid
            cpmc = cpml[0].cpmc
            pfbh = cpml[0].pbbh_id
            pfmc = cpml[0].pbbh.pbname
            return JsonResponse({'cpbh': cpbh, 'cpmc': cpmc, 'pfbh': pfbh, 'pfmc': pfmc})
        else:
            return JsonResponse({'product_null': ''})
    # 查询生产计划，判断有无此单号
    elif num == 3:
        spl = request.GET.get('spl')
        original = request.GET.get('Original')
        bool = 1
        if spl == original:
            return JsonResponse({'bool': bool})
        scjhb = Scjhb.objects.filter(spl=spl)
        if scjhb:
            bool = 0
        return JsonResponse({'bool': bool})
    # 查询计划明细表，判断有无此生产批号
    elif num == 4:
        scph = request.GET.get('scph')
        arr = request.GET.getlist('arr')
        scph_bool = 1
        if arr.count(scph):
            return JsonResponse({'scph_bool': scph_bool})
        todaywork = Todaywork.objects.filter(pk=scph)
        if todaywork:
            scph_bool = 0
        return JsonResponse({'scph_bool': scph_bool})


def update_production(request):
    '''
        修改生产计划时，由此视图处理
    '''
    user_name = request.GET.get('user_name')
    scjhb_bh = request.GET.get('scjhb_bh')
    scjhb = Scjhb.objects.get(spl=scjhb_bh)
    todaywork_list = scjhb.todaywork_set.all().order_by('ph')
    context = {
        'spl': scjhb.spl, 'scrq': scjhb.scrq, 'cpid': scjhb.cpid, 'sl': scjhb.sl, 'cs': scjhb.cs,
        'dw': scjhb.dw, 'zt': scjhb.zt, 'bz': scjhb.bz, 'bc': scjhb.bc, 'todaywork_list': todaywork_list,
        'title': '修改生产计划', 'user_name': user_name
    }
    return render(request, 'bc_production/production_update.html', context)


def add_production(request):
    '''
        增加生产计划时，由此视图处理
    '''
    user_name = request.GET.get('user_name')
    context = {
        'user_name': user_name, 'title': '增加生产计划'
    }
    return render(request, 'bc_production/production_add.html', context)


def file(request):
    pass


@transaction.atomic()
def production_save(request):
    '''
        保存生产计划时，由此视图处理
    '''
    new_scsl = []
    new_scxh = []
    new_scbc = []
    if request.method == 'POST':
        proof = request.POST.get('proof')
        print('--------------------------')
        print(proof)
        print('------------------------------')
        spl = request.POST.get('spl')

        scrq = request.POST.get('scrq')
        cpid = request.POST.get('cpid')
        sl = request.POST.get('sl')
        cs = request.POST.get('cs')
        dw = request.POST.get('dw')
        bc = request.POST.get('bc')
        bz = request.POST.get('bz')
        xdr = request.POST.get('xdr')
        zt = request.POST.get('zt', 0)
        scph = request.POST.getlist('scph')
        jhrq = request.POST.getlist('jhrq')
        scsx = request.POST.getlist('scsx')
        cpbh = request.POST.getlist('cpbh')
        cpmc = request.POST.getlist('cpmc')
        pfbh = request.POST.getlist('pfbh')
        pfmc = request.POST.getlist('pfmc')
        rwcs = request.POST.getlist('rwcs')
        scsl = request.POST.getlist('scsl')
        scxh = request.POST.getlist('scxh')
        scbz = request.POST.getlist('scbz')
        scbc = request.POST.getlist('scbc')
        pattern = re.compile(r'\.+')
        if (spl == '' or scrq == '' or cpid == '' or sl == '' or pattern.search(sl) or xdr == '' or scph == [] or
                jhrq == [] or scsx == [] or cpbh == [] or cpmc == [] or
                pfbh == [] or pfmc == [] or rwcs == []):
            return render(request, 'bc_production/production_add1.html')
        if not cs.isdigit():
            cs = None
        if not bc.isdigit():
            bc = None
        zt = True if zt == '1' else False
        user = User.objects.get(username=xdr)
        num = len(scph)
        for scsl_single in scsl:
            if scsl_single == '':
                scsl_single = None
                new_scsl.append(scsl_single)
            else:
                new_scsl.append(scsl_single)
        for scxh_single in scxh:
            if scxh_single == '':
                scxh_single = None
                new_scxh.append(scxh_single)
            else:
                new_scxh.append(scxh_single)
        for scbc_single in scbc:
            if scbc_single == '':
                scbc_single = None
                new_scbc.append(scbc_single)
            else:
                new_scbc.append(scbc_single)
        if not proof:
            scjhb = Scjhb.objects.create(spl=spl, scrq=scrq, cpid_id=cpid, sl=sl, cs=cs, dw=dw, zt=zt, bz=bz, bc=bc,
                                         xdr_id=user.id)
            for j in range(num):
                Todaywork.objects.create(ph=scph[j], spl_id=scjhb, pldate=jhrq[j], workno=scsx[j], cpid=cpbh[j], cpname=cpmc[j],
                                        pbbh=pfbh[j], pbname=pfmc[j], worksl=rwcs[j], plsl=new_scsl[j], scxh=new_scxh[j],
                                        bz=scbz[j], bc=new_scbc[j], zt=zt)
            return redirect('/admin/bc_production/scjhb/')
        else:
            todaywork_list = Scjhb.objects.get(spl=proof).todaywork_set.all()
            Todaywork.objects.filter(ph__in=todaywork_list).delete()
            a = Scjhb.objects.filter(spl=proof)
            a.update(spl=spl, scrq=scrq, cpid_id=cpid, sl=sl, cs=cs, dw=dw, zt=zt, bz=bz,
                                                   bc=bc, xdr_id=user.id)
            #scjhb = Scjhb.objects.filter(spl=proof).update(spl=spl, scrq=scrq, cpid_id=cpid, sl=sl, cs=cs, dw=dw, zt=zt, bz=bz,
            #                                       bc=bc, xdr_id=user.id)
            print('11111111111111111111111111111')
            print(a)
            print(spl)
            for j in range(num):
                Todaywork.objects.create(ph=scph[j], spl_id=a[0], pldate=jhrq[j], workno=scsx[j], cpid=cpbh[j], cpname=cpmc[j],
                                        pbbh=pfbh[j], pbname=pfmc[j], worksl=rwcs[j], plsl=new_scsl[j], scxh=new_scxh[j],
                                        bz=scbz[j], bc=new_scbc[j], zt=zt)
            return redirect('/admin/bc_production/scjhb/')
    else:
        return render(request, 'bc_production/production_add1.html')



'''
def a(request):
    num = [3, 4]
    name = ['中料', 'a']
    try:
        connection = psycopg2.connect(database='barcodesystem', user='postgres', password='941128', port=5432, host='localhost')
        cursor = connection.cursor()
        cursor.callproc('add_production', (num, name))
        connection.commit()
    except Exception as e:
        print(e)
        return HttpResponse('错误')
    else:
        cursor.close()
        connection.close()
        return HttpResponse('ok')
'''
