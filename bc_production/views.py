from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from bc_product.models import *
from django.core import serializers, paginator


def production_add(request):
    if request.method == 'POST':
        spl = request.POST.get('spl')
        rq = request.POST.get('rq')
        pbb = request.POST.get('jizhu', 0)
        return redirect('/admin/bc_formula/pb/')
    else:
        return render(request, 'bc_formula/formula_add.html')


def select_product(request, num):
    if num == 1:
        cpml_list = serializers.serialize('json', Cpml.objects.all())
        return JsonResponse({'cpml_list': cpml_list})
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
