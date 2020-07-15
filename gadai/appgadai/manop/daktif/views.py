from datetime import timedelta
import datetime
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from gadai.appgadai.models import AkadGadai,Barang,Kondisi_AktifB
from gadai.appgadai.manop.daktif.forms import DataAktifnaForm
from django.http import HttpResponse, Http404, HttpResponseRedirect

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('KEPALAGUDANG','administrator','MANOP')))
def show_data_bap(request,pk):
    data= Barang.objects.get(id=pk)
    akad = AkadGadai.objects.get(barang__id = data.id)
    return render(request,'manop/laporan/aktif/show_sts_aktif.html',{'data':data,'akad':akad})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('KEPALAGUDANG','administrator','MANOP')))
def data_kredit_kmr(request):
    kemarin = datetime.date.today() - timedelta(days=1)
    data = AkadGadai.objects.filter(tanggal = kemarin)
    return render(request,'manop/laporan/aktif/data_barang_aktif.html',{'data':data})

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('KEPALAGUDANG','administrator','MANOP')))
def input_bapna(request,pk):
    user = request.user
    data = get_object_or_404(AkadGadai,id = pk)
    barangna = Barang.objects.get(id = data.barang.id)
    if request.method == "POST":
        form = DataAktifnaForm(request.POST,data)
        if form.is_valid():
            charger = form.cleaned_data['charger']
            kondisi_charger = form.cleaned_data['kondisi_charger']
            batre = form.cleaned_data['batre']
            kondisi_batre = form.cleaned_data['kondisi_batre']
            keybord = form.cleaned_data['keybord']
            kondisi_keybord = form.cleaned_data['kondisi_keybord']
            cassing = form.cleaned_data['cassing']
            kondisi_cassing = form.cleaned_data['kondisi_cassing']

            layar = form.cleaned_data['layar']
            kondisi_layar = form.cleaned_data['kondisi_layar']
            lensa = form.cleaned_data['lensa']
            kondisi_lensa = form.cleaned_data['kondisi_lensa']
            batre_kamera = form.cleaned_data['batre_kamera']
            kondisi_batre_kamera = form.cleaned_data['kondisi_batre_kamera']
            cassing_kamera = form.cleaned_data['cassing_kamera']
            kondisi_cassing_kamera = form.cleaned_data['kondisi_cassing_kamera']

            layar_tv = form.cleaned_data['layar_tv']
            kondisi_layar_tv = form.cleaned_data['kondisi_layar_tv']
            remote = form.cleaned_data['remote']
            kondisi_remote = form.cleaned_data['kondisi_remote']

            harddisk  = form.cleaned_data['harddisk']
            kondisi_harddisk = form.cleaned_data['kondisi_harddisk']
            stick  = form.cleaned_data['stick']
            kondisi_stick = form.cleaned_data['kondisi_stick']
            hdmi  = form.cleaned_data['hdmi']
            kondisi_hdmi = form.cleaned_data['kondisi_hdmi']
            keterangan = form.cleaned_data['keterangan']
            simpan =  Kondisi_AktifB(baktif= barangna,cu = user,mu =user,tanggal= datetime.date.today(),charger=charger,
                kondisi_charger=kondisi_charger,batre=batre,kondisi_batre=kondisi_batre, keybord=keybord,cassing= cassing,
                kondisi_cassing= kondisi_cassing,layar=layar,kondisi_layar=kondisi_layar,lensa=lensa
                ,kondisi_lensa=kondisi_lensa,batre_kamera=batre_kamera,kondisi_batre_kamera=kondisi_batre_kamera,cassing_kamera=cassing_kamera,
                kondisi_cassing_kamera= kondisi_cassing_kamera,layar_tv=layar_tv,kondisi_layar_tv=kondisi_layar_tv,remote=remote,
                kondisi_remote=kondisi_remote,harddisk=harddisk,kondisi_harddisk= kondisi_harddisk,stick=stick,
                kondisi_stick=kondisi_stick,hdmi =hdmi,kondisi_hdmi=kondisi_hdmi,keterangan=keterangan)
            simpan.save()
            messages.add_message(request, messages.INFO, 'Data Penambahan Status Berhasil.')
            return HttpResponseRedirect('/manop/dlapur/data_kredit_kmr/' )
    else:
        form = DataAktifnaForm()
    return render(request,'manop/laporan/aktif/input_barang_aktif.html',{'data':data,'form':form})


