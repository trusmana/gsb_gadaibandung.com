from datetime import datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
import datetime, time
from gadai.appgadai.models import *

@login_required
def homepage(request):
    template_name = 'homepage.html'
    user = request.user
    try:
        cabang = user.get_profile().gerai
        if cabang:
            #akad_list = AkadGadai.objects.for_user(user)
            akad_list = AkadGadai.objects.for_user(user).all().filter(lunas__isnull=True).order_by('-tanggal')
            paginator = Paginator(akad_list, 30)

            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                akad_list = paginator.page(page)
            except (EmptyPage, InvalidPage):
                akad_list = paginator.page(paginator.num_pages) 
 
            template_name = 'home_gerai.html'
            variables = RequestContext(request, {'akad_list': akad_list,'cabang':cabang})
    except:
        variables = RequestContext(request, {})
    if user.is_staff:
        akad_list = Tbl_Cabang.objects.all().filter(kode_unit=300)
        kp = []
        for k in akad_list:
            if k.akadgadai_set.all().count() > 0:
                kp.append(k)
        
        total_piutang = total_akad= total_lunas = total_jt = total_nilai = total_jt_nilai = total_aktif = 0
        total_nilai_lunas = total_lelang= total_nilai_lelang= total_laba_lelang= total_all_barang= 0
        for k in kp :        
            total_piutang += k.piutang()
            total_akad += k.aktif()
            total_nilai += k.get_jumlah_nilai()
            total_jt += k.total_jatuhtempo()
            total_jt_nilai +=k.get_jumlah_jatuhtempo()
            total_lunas +=k.get_banyak_lunas()
            #total_nilai_lunas +=k.plns_nilai_bulanan()
            total_lelang +=k.get_banyak_lelang()
            total_nilai_lelang += k.get_total_nilailelang()
            total_all_barang +=k.total_barang()
        template_name = 'home_admin.html'
        variables = RequestContext(request, {'akad_list': akad_list,'kp':kp,
            'nkp' : len(kp),
            'total':total_akad,
            'tot_nilai':total_nilai,
            'tot_jatuh':total_jt,
            'tot_jt_nilai':total_jt_nilai,
            'tot_lunas':total_lunas,
            #'tot_nilai_lunas':total_nilai_lunas,
            'tot_lelang':total_lelang,
            'tot_nilai_lelang':total_nilai_lelang,
            #'tot_laba_lelang':total_laba_lelang,
            'tot_all_barang':total_all_barang,})
    return render_to_response(template_name, variables)
