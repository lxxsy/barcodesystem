from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse
# 序列化数据
from django.core import serializers
# 远程连接数据库包
from django.db import connection, transaction
from bc_formula.models import *
import re


# 供应商ajax查询判断函数
def query_gys(request, num):
    # 值为1操作供应商代码字段
    if num == 1:
        gyscode = request.GET.get('gyscode')
        original_code = request.GET.get('Original_code')
        bool_gys = 1
        # 若新值与原值相同，说明未作修改，bool_gys=1返回True，正确
        if not gyscode == original_code:
            # 两值不同则对新值进行查询，返回True说明已有此数据，不能修改返回False，错误
            if Gys.objects.filter(gyscode=gyscode).exists():
                bool_gys = 0
        return JsonResponse({'bool_gys': bool_gys})
    # 值为2操作供应商名称字段
    if num == 2:
        gysname = request.GET.get('gysname')
        original_name = request.GET.get('Original_name')
        bool_gys = 1
        # 若新值与原值相同，说明未作修改，bool_gys=1返回True，正确
        if not gysname == original_name:
            # 两值不同则对新值进行查询，返回True说明已有此数据，不能修改返回False，错误
            if Gys.objects.filter(gysname=gysname).exists():
                bool_gys = 0
        return JsonResponse({'bool_gys': bool_gys})


# 供应商修改页面数据获取函数
def update_gys(request):
    gys_id = request.GET.get('gys_id')
    bool_gys = 1
    # 查询供应商表是否有此供应商代码，出现异常则进入except环节
    try:
        gys = Gys.objects.get(gyscode=gys_id)
    # 出现错误，将错误返回到前端
    except Exception as e:
        print(e)
        return JsonResponse({'bool_gys': e})
    # 没有错误，讲此行数据的信息提取出来，填充到修改页面
    else:
        gyscode = gys.gyscode
        gysname = gys.gysname
        addr = gys.addr
        tel = gys.tel
        fax = gys.fax
        men = gys.men
        emai = gys.emai
        web = gys.web
        memo = gys.memo
        scdz = gys.scdz
        yyzzbh = gys.yyzzbh
        return JsonResponse({'bool_gys': bool_gys, 'gyscode': gyscode, 'gysname': gysname, 'addr': addr, 'tel': tel, 'fax': fax,
                             'men': men, 'emai': emai, 'web': web, 'memo': memo, 'scdz': scdz, 'yyzzbh': yyzzbh})


# 保存供应商信息到数据库
def save_gys(request):
    if request.method == 'POST':
        proof = request.POST.get('proof')  # 作用:判断是新增数据还是修改数据。如在修改页面进行的提交，则此变量不为''，
        gyscode = request.POST.get('gyscode')
        gysname = request.POST.get('gysname')
        addr = request.POST.get('addr')
        tel = request.POST.get('tel')
        fax = request.POST.get('fax')
        emai = request.POST.get('emai')
        web = request.POST.get('web')
        yyzzbh = request.POST.get('yyzzbh')
        men = request.POST.get('men')
        scdz = request.POST.get('scdz')
        memo = request.POST.get('memo')
        addanother = request.POST.get('_addanother')  # 按钮含义:保存并增加另一个，没有选择此按钮时为None
        add_edit = request.POST.get('_continue')  # 按钮含义:保存并继续编辑，没有选择此按钮时为None
        # 判断一些必填字段的值是否为空，为空则重定向到新增供应商页面
        if gyscode == '' or gysname == '':
            return redirect('/admin/bc_rmaterial/gys/add/')
        # 连接数据库，得到一个游标
        cursor = connection.cursor()
        # proof为空说明是新增数据
        if not proof:
            try:
                cursor.callproc('gys_I', (gyscode, gysname, addr, tel, fax, men, emai, web, memo, scdz, yyzzbh))
                connection.commit()
                cursor.close()
                connection.close()
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/gys/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/gys/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_rmaterial/gys/' + gyscode + '/update/')
            except Exception as e:
                print(e)
                cursor.close()
                connection.close()
                return redirect('/admin/bc_rmaterial/gys/add/')
        # 不为空则说明是修改已有数据
        else:
            try:
                cursor.callproc('gys_U', (gyscode, gysname, addr, tel, fax, men, emai, web, memo, scdz, yyzzbh, proof))
                connection.commit()
                cursor.close()
                connection.close()
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/gys/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/gys/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_rmaterial/gys/' + gyscode + '/update/')
            except Exception as e:
                print(e)
                cursor.close()
                connection.close()
                return redirect('/admin/bc_rmaterial/gys/add/')


# 原料入库ajax查询判断函数
def query_enterstock(request, num):
    # 值为1获取原料基础信息与原料仓库信息
    if num == 1:
        # 因QuerySet类型不能直接当作json字符串类型传递过去，所以需要先转换为json字符串类型
        ylinfo_list = serializers.serialize('json', Ylinfo.objects.all())
        stockinfo_list = serializers.serialize('json', Stockinfo.objects.all())
        return JsonResponse({'ylinfo_list': ylinfo_list, 'stockinfo_list': stockinfo_list})
    # 值为2判断此原料基础信息是否存在,此原料是否有合格供应商 【查询条件为原料代码】
    if num == 2:
        ylid = request.GET.get('ylid')
        # Original_ylid = request.GET.get('Original_ylid')
        ylid_bool = 0
        ylinfo_hgml_bool = 0
        ylname = ''
        piedw = ''
        stockname = ''
        ylid_list = Ylinfo.objects.filter(ylid=ylid)
        # 有此原料信息时，获取此行的数据
        if ylid_list.exists():
            ylid_bool = 1
            ylname = ylid_list[0].ylname
            piedw = ylid_list[0].piedw
            stockname = ylid_list[0].stockid.stockname
            # 分支判断，获取此原料信息的所以的合格供应商
            ylinfo_hgml = Ylinfo_HGML.objects.filter(ylid=ylid)
            # 有合格供应商则进行序列化，转化为json类型
            if ylinfo_hgml.exists():
                ylinfo_hgml_bool = 1
                ylinfo_hgml = serializers.serialize('json', ylinfo_hgml)
            # 没有合格供应商，将空[]赋值给ylinfo_hgml变量
            else:
                ylinfo_hgml = []
        # 无此原料信息时，将空[]赋值给ylinfo_hgml变量，其余需传递的参数均为默认值
        else:
            ylinfo_hgml = []
            # ylinfo_hgml_bool = 1
        return JsonResponse({'ylid_bool': ylid_bool, 'ylname': ylname, 'ylinfo_hgml': ylinfo_hgml,
                             'ylinfo_hgml_bool': ylinfo_hgml_bool, 'piedw': piedw, 'stockname': stockname})
    if num == 3:
        ylname = request.GET.get('ylname')
        # Original_ylname = request.GET.get('Original_ylname')
        ylname_bool = 0
        ylinfo_hgml_bool = 0
        ylid = ''
        piedw = ''
        stockname = ''
        ylname_list = Ylinfo.objects.filter(ylname=ylname)
        if ylname_list:
            ylname_bool = 1
            ylid = ylname_list[0].ylid
            piedw = ylname_list[0].piedw
            stockname = ylname_list[0].stockid.stockname
            ylinfo_hgml = Ylinfo_HGML.objects.filter(ylname=ylname)
            if ylinfo_hgml:
                ylinfo_hgml_bool = 1
                ylinfo_hgml = serializers.serialize('json', ylinfo_hgml)
            else:
                ylinfo_hgml = []
        else:
            ylinfo_hgml = []
            ylinfo_hgml_bool = 1
        return JsonResponse({'ylname_bool': ylname_bool, 'ylid': ylid, 'ylinfo_hgml': ylinfo_hgml,
                             'ylinfo_hgml_bool': ylinfo_hgml_bool, 'piedw': piedw, 'stockname': stockname})
    if num == 4:
        gyscode = request.GET.get('gyscode')
        # Original_gyscode = request.GET.get('Original_gyscode')
        gyscode_bool = 0
        gysname = ''
        gyscode_list = Gys.objects.filter(gyscode=gyscode)
        if gyscode_list:
            gyscode_bool = 1
            gysname = gyscode_list[0].gysname
        return JsonResponse({'gyscode_bool': gyscode_bool, 'gysname': gysname})
    if num == 5:
        gysname = request.GET.get('gysname')
        # Original_gysname = request.GET.get('Original_gysname')
        gysname_bool = 0
        gyscode = ''
        gysname_list = Gys.objects.filter(gysname=gysname)
        if gysname_list:
            gysname_bool = 1
            gyscode = gysname_list[0].gyscode
        return JsonResponse({'gysname_bool': gysname_bool, 'gyscode': gyscode})
    if num == 6:
        ylid = request.GET.get('ylid')
        stock = Stock.objects.get(ylid=ylid)
        stock_quantity = stock.quantity
        return JsonResponse({'stock_quantity': stock_quantity})
    if num == 7:
        enterstock_id = request.GET.get('enterstock_id')
        ylid = request.GET.get('ylid')
        zl = request.GET.get('zl')
        bool = 0
        zl_float = float(zl)
        stock = Stock.objects.get(ylid=ylid)
        stock_quantity = stock.quantity
        if zl_float > stock_quantity:
            return JsonResponse({'bool': bool})
        else:
            Enterstock.objects.get(id=enterstock_id).delete()
            stock.qcsl = stock_quantity
            stock.quantity = stock_quantity - zl_float
            stock.save()
            bool = 1
        return JsonResponse({'bool': bool})


# 原料入库修改页面数据获取函数
def update_enterstock(request):
    enterstock_id = request.GET.get('enterstock_id')
    enterstock = Enterstock.objects.get(id=enterstock_id)
    bool = 1
    if enterstock:
        barcode = enterstock.barcode
        ylname = enterstock.ylname
        clph = enterstock.clph
        dbz = enterstock.dbz
        zl = enterstock.zl
        rdatetime = enterstock.rdate
        scrqtime = enterstock.scrq
        gysname = enterstock.gysname
        lotbar = enterstock.lotbar
        bz = enterstock.bz
        check1no = enterstock.check1no
        qcmen = enterstock.qcmen
        gyscode = enterstock.gyscode
        rkck = enterstock.rkck.stockname
        ylid = enterstock.ylid_id
        user = User.objects.get(username=qcmen)
        user_id = user.id
        ylinfo_hgml = Ylinfo_HGML.objects.filter(ylid=ylid)
        if ylinfo_hgml:
            ylinfo_hgml = serializers.serialize('json', ylinfo_hgml)
        rdate = str(rdatetime).split()[0]
        scrq = str(scrqtime).split()[0]
        return JsonResponse({'bool': bool, 'barcode': barcode, 'ylname': ylname, 'clph': clph, 'dbz': dbz, 'zl': zl,
                             'rdate': rdate, 'scrq': scrq, 'gysname': gysname, 'lotbar': lotbar, 'bz': bz,
                             'check1no': check1no, 'qcmen': qcmen, 'gyscode': gyscode, 'rkck': rkck, 'user_id': user_id, 'ylid': ylid, 'ylinfo_hgml': ylinfo_hgml})
    else:
        bool = 0
        return JsonResponse({'bool': bool})


# 保存原料入库信息到数据库
def save_enterstock(request):
    if request.method == 'POST':
        proof_id = request.POST.get('proof_id')
        proof_zl = request.POST.get('proof_zl')
        ylid = request.POST.get('data_enterstock_ylid')
        ylname = request.POST.get('data_enterstock_ylname')
        gyscode = request.POST.get('gyscode')
        gysname = request.POST.get('gysname')
        zl = request.POST.get('zl')
        rdate = request.POST.get('rdate')
        rkck = request.POST.get('data_enterstock_stockinfo')
        scrq = request.POST.get('scrq')
        clph = request.POST.get('clph')
        dbz = request.POST.get('dbz')
        lotbar = request.POST.get('lotbar')
        bz = request.POST.get('bz')
        check1no = request.POST.get('check1no')
        qcmen = request.POST.get('qcmen')
        addanother = request.POST.get('_addanother')
        add_edit = request.POST.get('_continue')
        if (ylid == '' or ylname == '' or gyscode == '' or gysname == '' or zl == '' or rdate == '' or
            rkck == '' or dbz == '' or check1no == '' or qcmen == ''):
            return redirect('/admin/bc_rmaterial/enterstock/add/')
        barcode = ylid + gyscode + rdate + clph
        stockinfo = Stockinfo.objects.get(stockname=rkck)
        stockid = stockinfo.stockid
        user = User.objects.get(id=qcmen)
        qcmen = user.username
        cursor = connection.cursor()
        if not proof_id:
            try:
                cursor.callproc('enterstock_I', (barcode, ylname, clph, dbz, zl, rdate, scrq, gysname, lotbar, bz,
                                                 check1no, qcmen, gyscode, stockid, ylid))
                connection.commit()
                cursor.close()
                connection.close()
                enterstock_list = Enterstock.objects.filter(ylid=ylid)
                enterstock_id = str(enterstock_list[0].id)
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/enterstock/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/enterstock/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_rmaterial/enterstock/' + enterstock_id + '/update/')
            except Exception as e:
                print(e)
                cursor.close()
                connection.close()
                return redirect('/admin/bc_rmaterial/enterstock/add/')
        else:
            try:
                proof_zl_float = float(proof_zl)
                proof_id_int = int(proof_id)
                cursor.callproc('enterstock_U', (barcode, ylname, clph, dbz, zl, rdate, scrq, gysname, lotbar, bz,
                                                 check1no, qcmen, gyscode, stockid, ylid, proof_id_int, proof_zl_float))
                connection.commit()
                cursor.close()
                connection.close()
                enterstock_list = Enterstock.objects.filter(ylid=ylid)
                enterstock_id = str(enterstock_list[0].id)
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/enterstock/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/enterstock/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_rmaterial/enterstock/' + enterstock_id + '/update/')
            except Exception as e:
                print(e)
                cursor.close()
                connection.close()
                return redirect('/admin/bc_rmaterial/enterstock/add/')


# 合格供应商ajax查询判断函数
def query_ylinfo_hgml(request, num):
    if num == 1:
        ylinfo_list = serializers.serialize('json', Ylinfo.objects.all())
        gys_list = serializers.serialize('json', Gys.objects.all())
        return JsonResponse({'ylinfo_list': ylinfo_list, 'gys_list': gys_list})
    if num == 2:
        ylid = request.GET.get('ylid')
        gyscode = request.GET.get('gyscode')
        Original_ylid = request.GET.get('Original_ylid')
        ylid_bool = 0
        ylinfo_hgml_bool = 0
        ylname = ''
        ylid_list = Ylinfo.objects.filter(ylid=ylid)
        ylinfo_hgml = Ylinfo_HGML.objects.filter(ylid=ylid, gyscode=gyscode)
        if ylid == Original_ylid:
            ylid_bool = 1
            ylname = ylid_list[0].ylname
            return JsonResponse({'ylid_bool': ylid_bool, 'ylname': ylname, 'ylinfo_hgml_bool': ylinfo_hgml_bool})
        if ylid_list:
            ylid_bool = 1
            ylname = ylid_list[0].ylname
        if ylinfo_hgml:
            ylinfo_hgml_bool = 1
        return JsonResponse({'ylid_bool': ylid_bool, 'ylname': ylname, 'ylinfo_hgml_bool': ylinfo_hgml_bool})
    if num == 3:
        ylname = request.GET.get('ylname')
        gyscode = request.GET.get('gyscode')
        Original_ylname = request.GET.get('Original_ylname')
        ylname_bool = 0
        ylinfo_hgml_bool = 0
        ylid = ''
        ylname_list = Ylinfo.objects.filter(ylname=ylname)
        ylinfo_hgml = Ylinfo_HGML.objects.filter(ylname=ylname, gyscode=gyscode)
        if ylname == Original_ylname:
            ylname_bool = 1
            ylid = ylname_list[0].ylid
            return JsonResponse({'ylname_bool': ylname_bool, 'ylid': ylid, 'ylinfo_hgml_bool': ylinfo_hgml_bool})
        if ylname_list:
            ylname_bool = 1
            ylid = ylname_list[0].ylid
        if ylinfo_hgml:
            ylinfo_hgml_bool = 1
        return JsonResponse({'ylname_bool': ylname_bool, 'ylid': ylid, 'ylinfo_hgml_bool': ylinfo_hgml_bool})
    if num == 4:
        gyscode = request.GET.get('gyscode')
        ylid = request.GET.get('ylid')
        Original_gyscode = request.GET.get('Original_gyscode')
        gyscode_bool = 0
        ylinfo_hgml_bool = 0
        gysname = ''
        gyscode_list = Gys.objects.filter(gyscode=gyscode)
        ylinfo_hgml = Ylinfo_HGML.objects.filter(gyscode=gyscode, ylid=ylid)
        if gyscode == Original_gyscode:
            gyscode_bool = 1
            gysname = gyscode_list[0].gysname
            return JsonResponse({'gyscode_bool': gyscode_bool, 'gysname': gysname, 'ylinfo_hgml_bool': ylinfo_hgml_bool})
        if gyscode_list:
            gyscode_bool = 1
            gysname = gyscode_list[0].gysname
        if ylinfo_hgml:
            ylinfo_hgml_bool = 1
        return JsonResponse({'gyscode_bool': gyscode_bool, 'gysname': gysname, 'ylinfo_hgml_bool': ylinfo_hgml_bool})
    if num == 5:
        gysname = request.GET.get('gysname')
        ylid = request.GET.get('ylid')
        Original_gysname = request.GET.get('Original_gysname')
        gysname_bool = 0
        ylinfo_hgml_bool = 0
        gyscode = ''
        gysname_list = Gys.objects.filter(gysname=gysname)
        ylinfo_hgml = Ylinfo_HGML.objects.filter(gysname=gysname, ylid=ylid)
        if gysname == Original_gysname:
            gysname_bool = 1
            gyscode = gysname_list[0].gyscode
            return JsonResponse({'gysname_bool': gysname_bool, 'gyscode': gyscode, 'ylinfo_hgml_bool': ylinfo_hgml_bool})
        if gysname_list:
            gysname_bool = 1
            gyscode = gysname_list[0].gyscode
        if ylinfo_hgml:
            ylinfo_hgml_bool = 1
        return JsonResponse({'gysname_bool': gysname_bool, 'gyscode': gyscode, 'ylinfo_hgml_bool': ylinfo_hgml_bool})


# 合格供应商修改页面数据获取函数
def update_ylinfo_hgml(request):
    ylinfo_hgml_id = request.GET.get('ylinfo_hgml_id')
    ylinfo_hgml = Ylinfo_HGML.objects.get(id=ylinfo_hgml_id)
    bool = 1
    if ylinfo_hgml:
        ylname = ylinfo_hgml.ylname
        gysname = ylinfo_hgml.gysname
        scxkzh = ylinfo_hgml.scxkzh
        cppzwh = ylinfo_hgml.cppzwh
        cpbzbh = ylinfo_hgml.cpbzbh
        jkcpdjz = ylinfo_hgml.jkcpdjz
        bz = ylinfo_hgml.bz
        gyscode = ylinfo_hgml.gyscode_id
        ylid = ylinfo_hgml.ylid_id
        return JsonResponse({'bool': bool, 'ylname': ylname, 'gysname': gysname, 'scxkzh': scxkzh, 'cppzwh': cppzwh,
                             'cpbzbh': cpbzbh, 'jkcpdjz': jkcpdjz, 'bz': bz, 'gyscode': gyscode, 'ylid': ylid})
    else:
        bool = 0
        return JsonResponse({'bool': bool})


# 保存合格供应商信息到数据库
def save_ylinfo_hgml(request):
    if request.method == 'POST':
        proof_ylid = request.POST.get('proof_ylid')
        proof_gyscode = request.POST.get('proof_gyscode')
        ylid = request.POST.get('data_ylinfo_hgml_ylid')
        ylname = request.POST.get('data_ylinfo_hgml_ylname')
        gyscode = request.POST.get('data_ylinfo_hgml_gyscode')
        gysname = request.POST.get('data_ylinfo_hgml_gysname')
        scxkzh = request.POST.get('scxkzh')
        cppzwh = request.POST.get('cppzwh')
        cpbzbh = request.POST.get('cpbzbh')
        jkcpdjz = request.POST.get('jkcpdjz')
        bz = request.POST.get('bz')
        addanother = request.POST.get('_addanother')
        add_edit = request.POST.get('_continue')
        if ylid == '' or ylname == '' or gyscode == '' or gysname == '':
            return redirect('/admin/bc_rmaterial/ylinfo_hgml/add/')
        cursor = connection.cursor()
        if not proof_ylid:
            try:
                cursor.callproc('ylinfo_hgml_I', (ylname, gysname, scxkzh, cppzwh, cpbzbh, jkcpdjz, bz, gyscode, ylid))
                connection.commit()
                cursor.close()
                connection.close()
                ylinfo_hgml_list = Ylinfo_HGML.objects.filter(ylid=ylid, gyscode=gyscode)
                ylinfo_hgml_id = str(ylinfo_hgml_list[0].id)
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/ylinfo_hgml/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/ylinfo_hgml/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_rmaterial/ylinfo_hgml/' + ylinfo_hgml_id + '/update/')
            except Exception as e:
                print(e)
                cursor.close()
                connection.close()
                return redirect('/admin/bc_rmaterial/ylinfo_hgml/add/')
        else:
            try:
                cursor.callproc('ylinfo_hgml_U', (ylname, gysname, scxkzh, cppzwh, cpbzbh, jkcpdjz, bz, gyscode,
                                                  ylid, proof_ylid, proof_gyscode))
                connection.commit()
                cursor.close()
                connection.close()
                ylinfo_hgml_list = Ylinfo_HGML.objects.filter(ylid=ylid, gyscode=gyscode)
                ylinfo_hgml_id = str(ylinfo_hgml_list[0].id)
                if addanother is None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/ylinfo_hgml/')
                elif addanother is not None and add_edit is None:
                    return redirect('/admin/bc_rmaterial/ylinfo_hgml/add/')
                elif addanother is None and add_edit is not None:
                    return redirect('/admin/bc_rmaterial/ylinfo_hgml/' + ylinfo_hgml_id + '/update/')
            except Exception as e:
                print(e)
                cursor.close()
                connection.close()
                return redirect('/admin/bc_rmaterial/ylinfo_hgml/add/')


# 原料基础信息ajax查询判断函数
def query_rmaterial(request, num):
    if num == 1:
        ylfl_list = serializers.serialize('json', Ylfl.objects.all())
        stockinfo_list = serializers.serialize('json', Stockinfo.objects.all())
        return JsonResponse({'ylfl_list': ylfl_list, 'stockinfo_list': stockinfo_list})
    if num == 2:
        ylid = request.GET.get('ylid')
        original = request.GET.get('Original')
        bool = 1
        if ylid == original:
            return JsonResponse({'bool': bool})
        ylinfo_list = Ylinfo.objects.filter(ylid=ylid)
        if ylinfo_list:
            bool = 0
        return JsonResponse({'bool': bool})
    if num == 3:
        ylname = request.GET.get('ylname')
        original_name = request.GET.get('Original_name')
        bool = 1
        if ylname == original_name:
            return JsonResponse({'bool': bool})
        ylinfo_list = Ylinfo.objects.filter(ylname=ylname)
        if ylinfo_list:
            bool = 0
        return JsonResponse({'bool': bool})


# 原料基础信息修改页面数据获取函数
def update_rmaterial(request):
    ylinfo_id = request.GET.get('ylinfo_id')
    ylinfo = Ylinfo.objects.get(ylid=ylinfo_id)
    bool = 1
    if ylinfo:
        ylid = ylinfo.ylid
        ylname = ylinfo.ylname
        dw = ylinfo.dw
        piedw = ylinfo.piedw
        zbq = ylinfo.zbq
        goodzbq = ylinfo.goodzbq
        park = ylinfo.park
        pieprice = ylinfo.pieprice
        minsl = ylinfo.minsl
        maxsl = ylinfo.maxsl
        zf_name = ylinfo.zf.flmc
        zf_id = ylinfo.zf.flid
        stockid_name = ylinfo.stockid.stockname
        stockid = ylinfo.stockid.stockid
        tymc = ylinfo.tymc
        ysbz = ylinfo.ysbz
        barcode = ylinfo.barcode
        bz = ylinfo.bz
        ylzt = ylinfo.ylzt
        if pieprice is None:
            pieprice = ''
        return JsonResponse({'bool': bool, 'ylid': ylid, 'ylname': ylname, 'dw': dw, 'piedw': piedw,
                             'zbq': zbq, 'goodzbq': goodzbq, 'park': park, 'pieprice': pieprice,
                             'minsl': minsl, 'maxsl': maxsl, 'zf_name': zf_name, 'zf_id': zf_id, 'stockid_name': stockid_name,
                             'stockid': stockid, 'tymc': tymc, 'ysbz': ysbz, 'barcode': barcode, 'bz': bz, 'ylzt': ylzt})
    else:
        bool = 0
        return JsonResponse({'bool': bool})


# 保存原料基础信息到数据库
def save_rmaterial(request):
    proof = request.POST.get('proof')
    ylid = request.POST.get('ylid')
    ylname = request.POST.get('ylname')
    dw = request.POST.get('dw')
    piedw = request.POST.get('piedw')
    zbq = request.POST.get('zbq')
    goodzbq = request.POST.get('goodzbq')
    park = request.POST.get('park')
    pieprice = request.POST.get('pieprice')
    minsl = request.POST.get('minsl')
    maxsl = request.POST.get('maxsl')
    zf = request.POST.get('zf')
    stockid = request.POST.get('stockid')
    tymc = request.POST.get('tymc')
    ysbz = request.POST.get('ysbz')
    barcode = request.POST.get('barcode')
    bz = request.POST.get('bz')
    ylzt = request.POST.get('ylzt', 0)
    addanother = request.POST.get('_addanother')
    add_edit = request.POST.get('_continue')
    ylzt = True if ylzt == '1' else False
    pattern = re.compile(r'\.+')  # 制作re规则：对.进行转义，判断数据是否有.如果有则为True
    if (ylid == '' or ylname == '' or dw == '' or piedw == '' or stockid == '' or zf == '' or pattern.search(zbq) or
            pattern.search(goodzbq) or pattern.search(park) or pattern.search(minsl) or pattern.search(maxsl)):
        return redirect('/admin/bc_rmaterial/ylinfo/add/')
    if not zbq.isdigit():
        zbq = None
    if not goodzbq.isdigit():
        goodzbq = None
    if not park.isdigit():
        park = None
    if not pieprice:
        pieprice = None
    if not minsl.isdigit():
        minsl = None
    if not maxsl.isdigit():
        maxsl = None
    cursor = connection.cursor()
    if not proof:
        try:
            cursor.callproc('ylinfo_I', (ylid, ylname, dw, piedw, zbq, goodzbq, park, pieprice, minsl, maxsl, tymc,
                                         ysbz, ylzt, barcode, bz, stockid, zf))
            connection.commit()
            cursor.close()
            connection.close()
            if addanother is None and add_edit is None:
                return redirect('/admin/bc_rmaterial/ylinfo/')
            elif addanother is not None and add_edit is None:
                return redirect('/admin/bc_rmaterial/ylinfo/add/')
            elif addanother is None and add_edit is not None:
                return redirect('/admin/bc_rmaterial/ylinfo/' + ylid + '/update/')
        except Exception as e:
            print(e)
            cursor.close()
            connection.close()
            return redirect('/admin/bc_rmaterial/ylinfo/add/')
    else:
        try:
            cursor.callproc('ylinfo_U', (ylid, ylname, dw, piedw, zbq, goodzbq, park, pieprice, minsl, maxsl, tymc,
                                         ysbz, ylzt, barcode, bz, stockid, zf, proof))
            connection.commit()
            cursor.close()
            connection.close()
            if addanother is None and add_edit is None:
                return redirect('/admin/bc_rmaterial/ylinfo/')
            elif addanother is not None and add_edit is None:
                return redirect('/admin/bc_rmaterial/ylinfo/add/')
            elif addanother is None and add_edit is not None:
                return redirect('/admin/bc_rmaterial/ylinfo/' + ylid + '/update/')
        except Exception as e:
            print(e)
            cursor.close()
            connection.close()
            return redirect('/admin/bc_rmaterial/ylinfo/add/')


# 原料结存ajax查询判断函数
def query_stock(request, num):
    if num == 1:
        stockinfo_list = Stockinfo.objects.all().order_by('stockid')
        stockid = stockinfo_list[0].stockid
        stock_list = serializers.serialize('json', Stock.objects.filter(stockid=stockid).order_by('id'))
        stockinfo_list = serializers.serialize('json', stockinfo_list)
        return JsonResponse({'stockinfo_list': stockinfo_list, 'stock_list': stock_list})
    if num == 2:
        stockinfo_name = request.GET.get('stockinfo_name')
        stockinfo = Stockinfo.objects.get(stockname=stockinfo_name)
        stockinfo_id = stockinfo.stockid
        stock_list = serializers.serialize('json', Stock.objects.filter(stockid=stockinfo_id).order_by('id'))
        return JsonResponse({'stock_list': stock_list})