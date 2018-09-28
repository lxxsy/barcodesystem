from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from bc_formula.models import *
import psycopg2
import re


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
        zf = ylinfo.zf.flid
        stockid = ylinfo.stockid.stockid
        tymc = ylinfo.tymc
        ysbz = ylinfo.ysbz
        barcode = ylinfo.barcode
        bz = ylinfo.bz
        ylzt = ylinfo.ylzt
        return JsonResponse({'bool': bool, 'ylid': ylid, 'ylname': ylname, 'dw': dw, 'piedw': piedw,
                             'zbq': zbq, 'goodzbq': goodzbq, 'park': park, 'pieprice': pieprice,
                             'minsl': minsl, 'maxsl': maxsl, 'zf': zf, 'stockid': stockid, 'tymc': tymc,
                             'ysbz': ysbz, 'barcode': barcode, 'bz': bz, 'ylzt': ylzt})
    else:
        bool = 0
        return JsonResponse({'bool': bool})


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
    pattern = re.compile(r'\.+')
    if (ylid == '' or ylname == '' or dw == '' or piedw == '' or stockid == '' or zf == '' or pattern.search(zbq) or
            pattern.search(goodzbq) or pattern.search(park) or pattern.search(minsl) or pattern.search(maxsl) or
            pattern.search(ysbz)):
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
    if not ysbz.isdigit():
        ysbz = None
    connection = psycopg2.connect(database='barcodesystem', user='postgres', password='941128', port=5432, host='localhost')
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
        '''
        ylinfo = Ylinfo.objects.filter(ylid=proof)
        # pbf_list = ylinfo[0].pbf_set.all()
        ylinfo.update(ylid=ylid, ylname=ylname, dw=dw, piedw=piedw, zbq=zbq, goodzbq=goodzbq, park=park, pieprice=pieprice,
                      minsl=minsl, maxsl=maxsl, zf_id=zf, stockid_id=stockid, tymc=tymc, ysbz=ysbz, barcode=barcode,
                      bz=bz, ylzt=ylzt)
        if addanother is None and add_edit is None:
            return redirect('/admin/bc_rmaterial/ylinfo/')
        elif addanother is not None and add_edit is None:
            return redirect('/admin/bc_rmaterial/ylinfo/add/')
        elif addanother is None and add_edit is not None:
            return redirect('/admin/bc_rmaterial/ylinfo/' + ylinfo[0].ylid + '/update/')
        '''