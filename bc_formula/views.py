from django.shortcuts import render, redirect
from xadmin.views import BaseAdminView
from .models import *


def index1(request):
    if request.method == 'POST' and request.POST.get('uname'):
        pbbh = request.POST.get('uname')
        pb1 = request.POST.get('jizhu1', 0)
        pbb = request.POST.get('jizhu', 0)
        p = Pb()
        p.pbbh = pbbh
        p.sh = pb1
        p.yx = pbb
        p.save()
        return redirect('/admin/bc_formula/pb/')
    else:
        return render(request, 'bc_formula/formula_add.html')
