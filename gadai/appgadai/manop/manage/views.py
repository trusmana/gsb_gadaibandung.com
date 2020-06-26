from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gadai.appkeuangan.models import Menu,MenuItem
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from gadai.appgadai.manop.manage.forms import MenuItemForm
from django.template.loader import render_to_string
from gadai.appgadai.models import AkadGadai,Nasabah,Barang,ManopPelunasan,ManopPelunasanGu
import datetime


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('MANOP','administrator')))
def report_oto_pelunasan(request):
    start_date = datetime.date(2019,9,1)
    end_date = datetime.date.today()
    report = ManopPelunasanGu.objects.filter(status= 2).filter(tanggal__range=(start_date,end_date))
    return render(request,'manop/manage/report_oto_plns.html',{'report':report})


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
