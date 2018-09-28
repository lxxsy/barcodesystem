from django.shortcuts import render, redirect
from xadmin.views import BaseAdminView
from .models import *
from django.http import JsonResponse, HttpResponse
from bc_rmaterial.models import *
from django.core import serializers
import re
import psycopg2


def update_formula(request):
    '''
        修改配方时，由此视图处理
    '''
    pb_bh = request.GET.get('pb_bh')
    pb = Pb.objects.get(pbbh=pb_bh)
    pbbh = pb.pbbh
    pbname = pb.pbname
    pftype = pb.pftype
    scsx = pb.scsx
    scxh = pb.scxh
    yx = pb.yx
    bz = pb.bz
    pbf_list = serializers.serialize('json', pb.pbf_set.all().order_by('pk'))
    return JsonResponse({'pbbh': pbbh, 'pbname': pbname, 'pftype': pftype, 'scsx': scsx, 'scxh': scxh, 'yx': yx,
                         'bz': bz, 'pbf_list': pbf_list})


def save_formula(request):
    '''
        保存配方时，由此视图处理
    '''
    proof = request.POST.get('proof')
    pbbh = request.POST.get('pbbh')
    pbname = request.POST.get('pbname')
    pftype = request.POST.get('pftype')
    scsx = request.POST.get('scsx')
    scxh = request.POST.get('scxh')
    yx = request.POST.get('yx', 0)
    bz = request.POST.get('bz')
    addanother = request.POST.get('_addanother')
    add_edit = request.POST.get('_continue')
    plno = request.POST.getlist('plno')
    ylid = request.POST.getlist('datas')
    bzgl = request.POST.getlist('bzgl')
    topz = request.POST.getlist('topz')
    lowz = request.POST.getlist('lowz')
    dw = request.POST.getlist('dw')
    jno = request.POST.getlist('jno')
    hlt = request.POST.getlist('hlt')
    hzs = request.POST.getlist('hzs')
    print('-------------------')
    print(hlt)
    print('---------------------')
    yx = True if yx == '1' else False
    pattern = re.compile(r'\.+')
    if (pbbh == '' or pbname == '' or scsx == '' or scxh == '' or pattern.search(scsx) or pattern.search(scxh) or
            plno.count('') or ylid.count('') or bzgl.count('') or topz.count('') or lowz.count('') or jno.count('')):
        return redirect('/admin/bc_production/scjhb/add/')
    connection = psycopg2.connect(database='barcodesystem', user='postgres', password='941128', port=5432,
                                  host='localhost')
    cursor = connection.cursor()
    new_plno = []
    new_bzgl = []
    new_topz = []
    new_lowz = []
    new_jno = []
    new_hlt = []
    new_hzs = []
    for plno_single in plno:
        new_plno.append(int(plno_single))
    for bzgl_single in bzgl:
        new_bzgl.append(float(bzgl_single))
    for topz_single in topz:
        new_topz.append(float(topz_single))
    for lowz_single in lowz:
        new_lowz.append(float(lowz_single))
    for jno_single in jno:
        new_jno.append(int(jno_single))
    for hlt_single in hlt:
        if hlt_single == '1':
            new_hlt.append(True)
        else:
            new_hlt.append(False)
    for hzs_single in hzs:
        if hzs_single == '1':
            new_hzs.append(True)
        else:
            new_hzs.append(False)
    if not proof:
        try:
            cursor.callproc('pb_I', (pbbh, pbname, pftype, scsx, scxh, yx, bz, new_plno, new_bzgl, new_topz, new_lowz,
                                     dw, new_jno, new_hlt, new_hzs, ylid))
            connection.commit()
            cursor.close()
            connection.close()
            if addanother is None and add_edit is None:
                return redirect('/admin/bc_formula/pb/')
            elif addanother is not None and add_edit is None:
                return redirect('/admin/bc_formula/pb/add/')
            elif addanother is None and add_edit is not None:
                return redirect('/admin/bc_formula/pb/' + pbbh + '/update/')
        except Exception as e:
            print(e)
            cursor.close()
            connection.close()
            return redirect('/admin/bc_formula/pb/')  # 后续会返回一个错误页面
    else:
        try:
            cursor.callproc('pb_U', (pbbh, pbname, pftype, scsx, scxh, yx, bz, new_plno, new_bzgl, new_topz, new_lowz,
                                     dw, new_jno, new_hlt, new_hzs, ylid, proof))
            connection.commit()
            cursor.close()
            connection.close()
            if addanother is None and add_edit is None:
                return redirect('/admin/bc_formula/pb/')
            elif addanother is not None and add_edit is None:
                return redirect('/admin/bc_formula/pb/add/')
            elif addanother is None and add_edit is not None:
                return redirect('/admin/bc_formula/pb/' + pbbh + '/update/')
        except Exception as e:
            print(e)
            cursor.close()
            connection.close()
            return redirect('/admin/bc_formula/pb/')  # 后续会返回一个错误页面


def query_formula(request, num):
    if num == 1:
        ylinfo = serializers.serialize('json', Ylinfo.objects.all())
        return JsonResponse({'ylinfo': ylinfo})
    elif num == 2:
        pbbh = request.GET.get('pbbh')
        pb_list = Pb.objects.filter(pbbh=pbbh)
        bool = 1
        if pb_list:
            bool = 0
        return JsonResponse({'bool': bool})
    elif num == 3:
        plno = request.GET.get('plno')
        arr = request.GET.getlist('arr')
        plno_bool = 1
        if arr.count(plno):
            return JsonResponse({'plno_bool': plno_bool})
        pbf_list = Pbf.objects.filter(plno=plno)
        if pbf_list:
            plno_bool = 0
        return JsonResponse({'plno_bool': plno_bool})
    elif num == 4:
        current_value = request.GET.get('current_value')
        ylid = Ylinfo.objects.filter(ylid=current_value)
        ylid_bool = 0
        if ylid:
            ylid_bool = 1
        return JsonResponse({'ylid_bool': ylid_bool})
