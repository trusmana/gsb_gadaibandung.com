from django.shortcuts import render,redirect,render_to_response,RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gadai.appkeuangan.models import Menu,MenuItem
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from gadai.appgadai.manop.manage.forms import MenuItemForm
from django.template.loader import render_to_string
from gadai.appgadai.models import AkadGadai,Nasabah,Barang,ManopPelunasan,ManopPelunasanGu,TaksirHistory
from gadai.appkeuangan.models import Menu
import datetime

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('MANOP','administrator')))
def report_taksiran(request):
    user = request.user
    cek_menu = user.menuitem_set.all().count()
    cek_group = user.groups.all()
    menu = Menu.objects.filter(akses_grup__in=(cek_group)).filter(status_aktif = True)
    start_date = None
    end_date = None
    if 'start_date' in request.GET and request.GET['start_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        report = TaksirHistory.objects.filter(tglupdate__range=(start_date,end_date))
        variables=RequestContext(request,{'report':report,'start_date':start_date,'end_date':end_date,'menu':menu,
            'cek_menu':cek_menu})
        return render_to_response('manop/report_taksiran.html',variables)
    else:
        report = TaksirHistory.objects.filter(tglupdate__range=(start_date,end_date))
        return render(request,'manop/report_taksiran.html',{'report':report})
    return render(request,'manop/report_taksiran.html',{'start_date':start_date,'menu':menu})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('MANOP','administrator')))
def report_oto_pelunasan(request):
    user = request.user
    cek_menu = user.menuitem_set.all().count()
    cek_group = user.groups.all()
    menu = Menu.objects.filter(akses_grup__in=(cek_group)).filter(status_aktif = True)
    start_date = None
    end_date = None
    if 'start_date' in request.GET and request.GET['start_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        report = ManopPelunasanGu.objects.filter(status= 2).filter(tanggal__range=(start_date,end_date))
        lunas = AkadGadai.objects.filter(manoppelunasan__status= 2).filter(manoppelunasan__tanggal__range=(start_date,end_date))
        variables=RequestContext(request,{'report':report,'lunas':lunas,'start_date':start_date,'end_date':end_date,'menu':menu,
            'cek_menu':cek_menu})
        return render_to_response('manop/manage/report_oto_plns.html',variables)
    else:
        report = ManopPelunasanGu.objects.filter(status= 2).filter(tanggal__range=(start_date,end_date))
        return render(request,'manop/manage/report_oto_plns.html',{'report':report})
    return render(request,'manop/manage/report_oto_plns.html',{'start_date':start_date,'menu':menu})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('MANOP','administrator')))
def aktif_tombol_gu(request,object_id):
    barang = Barang.objects.get(id=object_id)
    barang.buka_tutup_gu = 0
    barang.save()
    messages.add_message(request, messages.INFO, 'Tombol Gadai Ulang telah Di buka')
    return HttpResponseRedirect('/manop/manage/list_cari_baru/')



@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('MANOP','administrator')))
def show_manop(request,object_id):
    nsb=Nasabah.objects.get(id=object_id)
    ag=nsb.akadgadai_set.all()
    p=ag.order_by('-tanggal')
    return render(request,'manop/manop_show.html',{'nsb':nsb,'ag':p})

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('MANOP','administrator')))
def list_cari_baru(request):
    daftar = None
    if ('q' in request.GET) and request.GET['q'].strip():
        data_cari = request.GET['q']
        daftar = Nasabah.objects.filter(nama__icontains=data_cari)
    return render(request,'manop/manop_cari_baru.html',{'daftar':daftar})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('MANOP','administrator')))
def menu_update(request, pk):
    menu = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,'Parameter Disimpan')
            return HttpResponseRedirect('manop/manage/menu_item/')
    else:
        form = MenuItemForm(instance=menu)
    return render(request, 'manop/laporan/menu_update.html', {'form': form,'id':pk})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='MANOP'))
def menu_item(request):
    menu = MenuItem.objects.filter(menu__status_aktif__isnull= False)
    list = []
    for a in menu:
        list.append({'akses_group':a.menu.akses_menu,'id':a.id,'judul':a.judul,'nama':a.menu.nama,'pengguna':a.user})
    return render(request, 'manop/laporan/menu_item.html', {'orders': list})
