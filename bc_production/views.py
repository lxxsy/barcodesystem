from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *


def production_add(request):
    if request.method == 'POST':
        spl = request.POST.get('spl')
        rq = request.POST.get('rq')
        pbb = request.POST.get('jizhu', 0)
        return redirect('/admin/bc_formula/pb/')
    else:
        return render(request, 'bc_formula/formula_add.html')


def detailed_list(request):
    total = int(request.GET.get('number', 0)) + 1
    # print(total)
    lists = []
    for i in range(total):
        lists.append(i)
    # print(lists)
    context = {
        'lists': lists
    }
    # return JsonResponse({'a': l})
    return render(request, 'bc_production/production_add.html', context)

