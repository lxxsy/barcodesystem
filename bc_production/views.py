from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from bc_product.models import *
from django.core import serializers, paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.db.models import Max
import re
import psycopg2
import datetime
from django.template.response import TemplateResponse


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
        current_value = request.GET.get('current_value')
        cpml = Cpml.objects.filter(cpid=current_value)
        cpml_bool = 0
        if cpml:
            cpml_bool = 1
        return JsonResponse({'cpml_bool': cpml_bool})


def update_production(request):
    '''
        修改生产计划时，由此视图处理
    '''

    # user_name = request.GET.get('user_name')
    scjhb_bh = request.GET.get('scjhb_bh')
    scjhb = Scjhb.objects.get(spl=scjhb_bh)
    spl = scjhb.spl
    scrq = scjhb.scrq
    cpid = scjhb.cpid.cpid
    username = scjhb.xdr.username
    sl = scjhb.sl
    cs = scjhb.cs
    dw = scjhb.dw
    zt = scjhb.zt
    bz = scjhb.bz
    bc = scjhb.bc
    todaywork_list = serializers.serialize('json', scjhb.todaywork_set.all().order_by('pk'))
    return JsonResponse({'spl': spl, 'scrq': scrq, 'cpid': cpid, 'username': username, 'sl': sl, 'cs': cs, 'dw': dw,
                         'zt': zt, 'bz': bz, 'bc': bc, 'todaywork_list': todaywork_list})


def add_production(request):
    '''
        增加生产计划时，由此视图处理(暂时废弃)
    '''
    user_name = request.GET.get('user_name')
    context = {
        'user_name': user_name, 'title': '增加生产计划'
    }
    return render(request, 'bc_production/production_add.html', context)
    # return render(request, 'bc_products/cpsm/2018/09/07/4号.html')


def production_save(request):
    '''
        保存生产计划时，由此视图处理
    '''
    proof = request.POST.get('proof')
    spl = request.POST.get('spl')
    scrq = request.POST.get('scrq')
    cpid = request.POST.get('datas')
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
    user = User.objects.get(username=xdr)
    pattern = re.compile(r'\.+')
    if (spl == '' or scrq == '' or cpid == '' or sl == '' or pattern.search(sl) or cs == '' or
            pattern.search(cs) or xdr == ''):
        return redirect('/admin/bc_production/scjhb/add/')
    if not bc.isdigit():
        bc = None
    connection = psycopg2.connect(database='barcodesystem', user='postgres', password='941128', port=5432,
                                  host='localhost')
    cursor = connection.cursor()
    if not proof:
        c_date = datetime.date.today()
        todyawork = Todaywork.objects.all().aggregate(Max('pk'))  # 取计划附表id的最大值
        todaywork_ph = todyawork.get('pk__max')
        if todaywork_ph is None:
            num_ber = 0
        else:
            ph = Todaywork.objects.filter(pk=todaywork_ph)[0].ph
            print('---------------')
            print(ph)
            str_date = ph[:8]
            if c_date.strftime('%Y%m%d') == str_date:
                num_ber = int(ph[8:])
            else:
                num_ber = 0
        try:
            cursor.callproc('scjhb_I', (spl, scrq, sl, cs, dw, bc, zt, bz, cpid, user.id, num_ber))
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
        new_jhrq = []
        new_scsx = []
        new_rwcs = []
        new_scsl = []
        new_scxh = []
        for jhrq_single in jhrq:
            new_jhrq.append(datetime.datetime.strptime(jhrq_single, '%Y-%m-%d').date())
        for scsx_single in scsx:
            new_scsx.append(int(scsx_single))
        for rwcs_single in rwcs:
            new_rwcs.append(int(rwcs_single))
        for scsl_single in scsl:
            new_scsl.append(int(scsl_single))
        for scxh_single in scxh:
            if scxh_single == '':
                scxh_single = None
                new_scxh.append(scxh_single)
            else:
                new_scxh.append(int(scxh_single))
        try:
            cursor.callproc('scjhb_U', (proof, spl, scrq, sl, cs, dw, bc, zt, bz, cpid, user.id, scph, new_jhrq,
                                        new_scsx, cpbh, cpmc, pfbh, pfmc, new_rwcs, new_scsl, new_scxh, scbz))
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
        '''
        todaywork_list = Scjhb.objects.get(spl=proof).todaywork_set.all()
        Todaywork.objects.filter(pk__in=todaywork_list).delete()
        scjhb = Scjhb.objects.filter(spl=proof)
        scjhb.update(spl=spl, scrq=scrq, cpid_id=cpid, sl=sl, cs=cs, dw=dw, zt=zt, bz=bz,
                     bc=bc, xdr_id=user.id)
        for j in range(num):
            Todaywork.objects.create(ph=scph[j], spl_id=scjhb[0], pldate=jhrq[j], workno=scsx[j], cpid=cpbh[j],
                                     cpname=cpmc[j],
                                     pbbh=pfbh[j], pbname=pfmc[j], worksl=rwcs[j], plsl=new_scsl[j], scxh=new_scxh[j],
                                     bz=scbz[j], zt=zt)
        if addanother is None and add_edit is None:
            return redirect('/admin/bc_production/scjhb/')
        elif addanother is not None and add_edit is None:
            return redirect('/admin/bc_production/scjhb/add/')
        elif addanother is None and add_edit is not None:
            return redirect('/admin/bc_production/scjhb/' + scjhb[0].spl + '/update/')
        '''


def a(request):
    d = []
    c = []
    a = [1, None, 2]
    b = ['2018-09-27', '2018-09-27']

    for i in b:
        d.append(datetime.datetime.strptime(i, '%Y-%m-%d').date())
    connection = psycopg2.connect(database='barcodesystem', user='postgres', password='941128', port=5432,
                                  host='localhost')
    cursor = connection.cursor()
    cursor.callproc('a_trigger', (a, d))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect('/admin/bc_production/scjhb/')
'''
@transaction.atomic()
def production_save1(request):
    
        保存生产计划时，由此视图处理(暂时废弃)
    
    new_scsl = []
    new_scxh = []
    if request.method == 'POST':
        proof = request.POST.get('proof')
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
        pattern = re.compile(r'\.+')
        if (spl == '' or scrq == '' or cpid == '' or sl == '' or pattern.search(sl) or xdr == '' or scph == [] or
                jhrq == [] or scsx == [] or cpbh == [] or cpmc == [] or
                pfbh == [] or pfmc == [] or rwcs == []):
            return redirect('/admin/bc_production/scjhb/add/')
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
        if not proof:
            scjhb = Scjhb.objects.create(spl=spl, scrq=scrq, cpid_id=cpid, sl=sl, cs=cs, dw=dw, zt=zt, bz=bz, bc=bc,
                                         xdr_id=user.id)
            for j in range(num):
                Todaywork.objects.create(ph=scph[j], spl_id=scjhb, pldate=jhrq[j], workno=scsx[j], cpid=cpbh[j], cpname=cpmc[j],
                                        pbbh=pfbh[j], pbname=pfmc[j], worksl=rwcs[j], plsl=new_scsl[j], scxh=new_scxh[j],
                                        bz=scbz[j], zt=zt)
            if addanother is None and add_edit is None:
                return redirect('/admin/bc_production/scjhb/')
            elif addanother is not None and add_edit is None:
                return redirect('/admin/bc_production/scjhb/add/')
            elif addanother is None and add_edit is not None:
                return redirect('/admin/bc_production/scjhb/'+scjhb.spl+'/update/')
        else:
            todaywork_list = Scjhb.objects.get(spl=proof).todaywork_set.all()
            Todaywork.objects.filter(ph__in=todaywork_list).delete()
            scjhb = Scjhb.objects.filter(spl=proof)
            scjhb.update(spl=spl, scrq=scrq, cpid_id=cpid, sl=sl, cs=cs, dw=dw, zt=zt, bz=bz,
                                                   bc=bc, xdr_id=user.id)
            for j in range(num):
                Todaywork.objects.create(ph=scph[j], spl_id=scjhb[0], pldate=jhrq[j], workno=scsx[j], cpid=cpbh[j], cpname=cpmc[j],
                                        pbbh=pfbh[j], pbname=pfmc[j], worksl=rwcs[j], plsl=new_scsl[j], scxh=new_scxh[j],
                                        bz=scbz[j], zt=zt)
            if addanother is None and add_edit is None:
                return redirect('/admin/bc_production/scjhb/')
            elif addanother is not None and add_edit is None:
                return redirect('/admin/bc_production/scjhb/add/')
            elif addanother is None and add_edit is not None:
                return redirect('/admin/bc_production/scjhb/'+scjhb[0].spl+'/update/')
    else:
        return render(request, 'bc_production/production_add.html')
'''
