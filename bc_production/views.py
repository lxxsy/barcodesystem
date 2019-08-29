from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from bc_product.models import *
from bc_rmaterial.models import *
from django.core import serializers
from django.db.models import Max
from django.db import connection, transaction
import re
import datetime


def query_production(request, num):
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
            pfsc = cpml[0].pbbh.scxh
            return JsonResponse({'cpbh': cpbh, 'cpmc': cpmc, 'pfbh': pfbh, 'pfmc': pfmc, 'pfsc': pfsc})
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
        todaywork = Todaywork.objects.filter(ph=scph)
        if todaywork:
            scph_bool = 0
        return JsonResponse({'scph_bool': scph_bool})
    elif num == 5:
        cpid = request.GET.get('cpid')
        cpml = Cpml.objects.filter(cpid=cpid)
        cpid_bool = 0
        cpmc = ''
        cpbh = ''
        pfbh = ''
        pfmc = ''
        pfsc = ''
        if cpml:
            cpid_bool = 1
            cpmc = cpml[0].cpmc
            cpbh = cpml[0].cpid
            pfbh = cpml[0].pbbh_id
            pfmc = cpml[0].pbbh.pbname
            pfsc = cpml[0].pbbh.scxh
        return JsonResponse({'cpid_bool': cpid_bool, 'cpmc': cpmc, 'cpbh': cpbh, 'pfbh': pfbh, 'pfmc': pfmc, 'pfsc': pfsc})
    elif num == 6:
        cpname = request.GET.get('cpname')
        cpml = Cpml.objects.filter(cpmc=cpname)
        cpname_bool = 0
        cpid = ''
        cpmc = ''
        pfbh = ''
        pfmc = ''
        pfsc = ''
        if cpml:
            cpname_bool = 1
            cpid = cpml[0].cpid
            cpmc = cpml[0].cpmc
            pfbh = cpml[0].pbbh_id
            pfmc = cpml[0].pbbh.pbname
            pfsc = cpml[0].pbbh.scxh
        return JsonResponse({'cpname_bool': cpname_bool, 'cpid': cpid, 'cpmc': cpmc, 'pfbh': pfbh, 'pfmc': pfmc, 'pfsc': pfsc})
    elif num == 7:
        scjhb_spl = request.GET.get('scjhb_spl')
        try:
            Todaywork.objects.filter(spl=scjhb_spl).delete()
            Llyl.objects.filter(spl=scjhb_spl).delete()
            Scjhb.objects.filter(spl=scjhb_spl).delete()
            bool = 1
        except Exception:
            bool = 0
        return JsonResponse({'bool': bool})


def update_production(request):
    '''
        修改生产计划时，由此视图处理
    '''
    scjhb_bh = request.GET.get('scjhb_bh')
    scjhb = Scjhb.objects.get(spl=scjhb_bh)
    spl = scjhb.spl
    scrq = scjhb.scrq
    cpid = scjhb.cpid_id
    cpname = scjhb.cpname
    user_id = scjhb.xdr_id
    sl = scjhb.sl
    cs = scjhb.cs
    dw = scjhb.dw
    zt = scjhb.zt
    bz = scjhb.bz
    bc = scjhb.bc
    if bc is None:
        bc = ''
    todaywork_list = serializers.serialize('json', scjhb.todaywork_set.all().order_by('pk'))
    return JsonResponse({'spl': spl, 'scrq': scrq, 'cpid': cpid, 'cpname': cpname, 'user_id': user_id, 'sl': sl,
                         'cs': cs, 'dw': dw, 'zt': zt, 'bz': bz, 'bc': bc, 'todaywork_list': todaywork_list})


def save_production(request):
    '''
        保存生产计划时，由此视图处理
    '''
    proof = request.POST.get('proof')
    spl = request.POST.get('spl')
    scrq = request.POST.get('scrq')
    cpid = request.POST.get('data_production_cpid')
    cpname = request.POST.get('data_production_cpname')
    sl = request.POST.get('sl')
    cs = request.POST.get('cs')
    dw = request.POST.get('dw')
    bc = request.POST.get('bc')
    bz = request.POST.get('bz')
    xdr = request.POST.get('xdr')
    zt = request.POST.get('zt', 0)
    addanother = request.POST.get('_addanother')
    add_edit = request.POST.get('_continue')
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
    zt = True if zt == '1' else False
    # user = User.objects.get(username=xdr)
    pattern_one = re.compile(r'^[1-9][0-9]?$')
    pattern_two = re.compile(r'^[0-9]+\.?[0-9]*$')
    pattern_three = re.compile(r'^0+\.?0*$')
    if (spl == '' or scrq == '' or cpid == '' or cpname == '' or sl == '' or cs == '' or xdr == '' or
            scph.count('') or jhrq.count('') or scsx.count('') or rwcs.count('') or scsl.count('')):
        return redirect('/admin/bc_production/scjhb/add/')
    if pattern_two.match(sl):
        if pattern_three.match(sl):
            return redirect('/admin/bc_production/scjhb/add/')
    else:
        return redirect('/admin/bc_production/scjhb/add/')
    if not pattern_one.match(cs):
        return redirect('/admin/bc_production/scjhb/add/')
    if not bc.isdigit():
        bc = None
    # 生成成品二维码的url
    special_batch_url = 'http://192.168.138.1:8000/product/quality_trace_back?SPL=%s' % spl
    cursor = connection.cursor()
    if not proof:
        if Scjhb.objects.filter(spl=spl):
            return redirect('/admin/bc_production/scjhb/add/')
        with transaction.atomic():
            # 获取当天的日期
            # c_date = datetime.date.today()
            if not SystemParameter.objects.all().exists():
                SystemParameter.objects.create(id='wybs', lldh=1, scph=1)
            # 取计划附表id的最大值,aggregate()为聚合函数，获取的结果值是一个字典{'pk__max': (pk值)或(None)}
            todaywork = Todaywork.objects.aggregate(Max('pk'))
            # 取键'pk__max'对应的值
            todaywork_ph = todaywork.get('pk__max')
            if todaywork_ph is None:  # 说明是新表，ph计数从0开始
                # 修改系统表的批号字段为数值1
                ph = '0'
            else:
                ph = Todaywork.objects.filter(pk=todaywork_ph)[0].ph  # 20180104001
        try:
            cursor.callproc('scjhb_I', (spl, scrq, cpname, sl, cs, dw, bc, zt, bz, cpid, xdr, ph, special_batch_url))
            connection.commit()
            cursor.close()
            connection.close()
            if addanother is None and add_edit is None:
                return redirect('/admin/bc_production/scjhb/')
            elif addanother is not None and add_edit is None:
                return redirect('/admin/bc_production/scjhb/add/')
            elif addanother is None and add_edit is not None:
                return redirect('/admin/bc_production/scjhb/' + spl + '/update/')
        except Exception as e:
            print(e)
            cursor.close()
            connection.close()
            return redirect('/admin/bc_production/scjhb/')  # 后续会返回一个错误页面
    else:
        new_jhrq = []   # 日期
        new_scsx = []   # 生产顺序
        new_rwcs = []   # 任务次数
        new_scsl = []   # 数量
        new_scxh = []   # 生产线号
        for jhrq_single in jhrq:
            new_jhrq.append(datetime.datetime.strptime(jhrq_single, '%Y-%m-%d').date())
        for scsx_single in scsx:
            new_scsx.append(int(scsx_single))
        for rwcs_single in rwcs:
            new_rwcs.append(int(rwcs_single))
        for scsl_single in scsl:
            new_scsl.append(float(scsl_single))
        for scxh_single in scxh:
            if scxh_single == '':
                scxh_single = None
                new_scxh.append(scxh_single)
            else:
                new_scxh.append(int(scxh_single))
        try:
            cursor.callproc('scjhb_U', (spl, scrq, cpname, sl, cs, dw, bc, zt, bz, cpid, xdr, scph, new_jhrq, new_scsx,
                                        cpbh, cpmc, pfbh, pfmc, new_rwcs, new_scsl, new_scxh, scbz, proof, special_batch_url))
            connection.commit()
            cursor.close()
            connection.close()
            if addanother is None and add_edit is None:
                return redirect('/admin/bc_production/scjhb/')
            elif addanother is not None and add_edit is None:
                return redirect('/admin/bc_production/scjhb/add/')
            elif addanother is None and add_edit is not None:
                return redirect('/admin/bc_production/scjhb/' + spl + '/update/')
        except Exception as e:
            print(e)
            cursor.close()
            connection.close()
            return redirect('/admin/bc_production/scjhb/')  # 后续会返回一个错误页面


def request_data(request):
    cpid = request.GET.get('cpid')
    spl = request.GET.get('spl')
    try:
        cpml = Cpml.objects.get(cpid=cpid)
        scjhb = Scjhb.objects.get(spl=spl)
    except Exception as e:
        print(e)
        return JsonResponse({'errors': '请重试'})
    else:
        # barcode = 'http://192.168.138.1:8000/product/quality_trace_back?SPL=%s' % scjhb.spl
        return JsonResponse({'cpid': cpml.cpid, 'spl': scjhb.spl})


