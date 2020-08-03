from datetime import timedelta
import datetime
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from gadai.appgadai.models import AkadGadai,Barang,Kondisi_AktifB,Check_Kg
from gadai.appgadai.manop.daktif.forms import DataAktifnaForm,Verivikasi
from django.http import HttpResponse, Http404, HttpResponseRedirect
from gadai.appkeuangan.report.forms import SearchForm,FilterNewForm
from django.template.loader import render_to_string
from django import forms
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os, string
from django.conf import settings
from gadai.appgadai.templatetags.number_format import number_format

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('KEPALAGUDANG','administrator','MANOP')))
def cetak_bap(request,pk,barang,check):
    akadgadai = AkadGadai.objects.get(id=pk)
    br = get_object_or_404(Barang ,pk=barang)
    at = get_object_or_404(Kondisi_AktifB,pk= check)
    tanggal_cetak = datetime.date.today()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "BA_%s_%s.pdf"' % (akadgadai.agnasabah.nama,akadgadai.norek())
    sekarang=datetime.datetime.now()
    sekarang=datetime.datetime.now()
    h=sekarang.day
    m=sekarang.month
    y=sekarang.year
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawRightString(450 , 765,"BERITA ACARA PEMERIKSAAN BARANG JAMINAN")
    p.setFont('Helvetica', 10)
    p.drawString(30,748,"Hari ini tanggal %s berdasarkan kewenangan yang ada, dilakukan pemeriksaan terhadap barang"  % ((akadgadai.tanggal.strftime('%d %B %Y'))))
    p.drawString(30,736,"jaminan.")
    p.drawString(30,712, "Nomor Rekening " )
    p.drawString(200,712, ": %s" % akadgadai.norek())
    p.drawString(30,700,"Nama Gerai")
    p.drawString(200,700,": %s " % akadgadai.gerai)
    p.drawString(30,688,"Atas Nama")
    p.drawString(200,688,": %s" % akadgadai.agnasabah.nama)
    p.drawString(30,676,"Jangka Waktu Pinjaman " )
    p.drawString(200,676,": %s s/d %s" % (akadgadai.tanggal.strftime('%d %B %Y'),akadgadai.jatuhtempo.strftime('%d %B %Y')))

    p.drawString(30,646,"Berdasarkan rincian yang ada barang jaminan tersebut terdiri: " )
    p.drawString(30,622,"Jenis Barang " )
    p.drawString(200,622,": %s " % (akadgadai.jenis_barang_all()))
    p.drawString(30,610,"Merk Barang " )
    p.drawString(200,610,": %s " % (akadgadai.merk_all()))

    p.drawString(30,598,"Type " )
    p.drawString(200,598,": %s %s " % (akadgadai.jenis_barang_all(),akadgadai.merk_all()))

    p.drawString(30,586,"Besar Uang Pinjaman " )
    p.drawString(200,586,": %s " % number_format(akadgadai.nilai))

    p.setFont('Helvetica', 10)
    p.drawString(30,567,"Permeriksaan Gerai " )
    p.drawString(260,567,"Gudang Aktif")

    p.line(30 , 564, 570 ,564  )

    p.drawString(30,552,"Keybord/ keypad " )
    p.drawString(130,552,": %s - %s  " %(br._keybord_cab(),br._kkeybord_cab()) )
    p.drawString(260,552,"Keybord/Keypad" )
    p.drawString(375,552,": %s - %s"% (at._keybord_aktif(),at._kkeybord_aktif()) )

    p.drawString(30,540,"Baterai " )
    p.drawString(130,540,": %s - %s " %(br._batre_cab(),br._kbatre_cab()))
    p.drawString(260,540,"Baterai" )
    p.drawString(375,540,": %s -%s" %(at._batre_aktif(),at._kbatre_aktif()) )

    p.drawString(30,528,"Charge " )
    p.drawString(130,528,": %s - %s  " %(br._charger_cab(),br._kcharger_cab()))
    p.drawString(260,528,"Charge" )
    p.drawString(375,528,": %s - %s"%(at._charger_aktif(),at._kcharger_aktif()) )

    p.drawString(30,516,"Password " )
    p.drawString(130,516,": %s " %(br._pass_cab()))
    p.drawString(260,516,"Password" )
    p.drawString(375,516,": %s" %(at._pass_aktif()))

    p.drawString(30,504,"Chasing " )
    p.drawString(130,504,": %s - %s " %(br._cassing_cab(),br._kcassing_cab()))
    p.drawString(260,504,"Chasing" )
    p.drawString(375,504,": Ada" )

    p.drawString(30,492,"Layar " )
    p.drawString(130,492,": %s - %s  " %(br._layar_cab(),br._klayar_cab()))
    p.drawString(260,492,"layar" )
    p.drawString(375,492,": Ada" )

    p.drawString(30,480,"Tas" )
    p.drawString(130,480,": %s " %(br._tas_cab()))
    p.drawString(260,480,"Tas" )
    p.drawString(375,480,": Ada" )

    p.drawString(30,468,"Dus " )
    p.drawString(130,468,": %s " %(br._dus_cab()))
    p.drawString(260,468,"Dus" )
    p.drawString(375,468,": Ada" )

    p.line(30 , 460, 570 ,460  )

    p.drawString(30,448,"Note Gerai " )
    p.drawString(130,448,": %s " %(br.accesoris_barang1))
    p.drawString(30,436,"Note Gudang Aktif" )
    p.drawString(130,436,": %s"%(at.keterangan) )


    #p.drawString(30,424,"Assisten Manajer Operasi")
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ttd_manop.png'), 0.5*inch, (0.7 + 3.75) * inch, width=60.5/17.5*0.51*inch,height=24/17.5*0.51*inch)

    p.drawString(60,388,"Diperiksa oleh,")
    p.drawString(250,388,"Mengetahui,")

    p.drawString(50,304,"Ferry Firdaus" )
    p.drawString(250,304,"Arie Rachadian R" )
    p.drawString(430,304,"Tedi Rusmana it" )


    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('KEPALAGUDANG','administrator','MANOP')))
def data_bap(request):
    data = Kondisi_AktifB.objects.exclude(check_kg__status= ('2','3'))
    return render(request,'manop/laporan/aktif/show_bapna.html',{'data':data})

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('KEPALAGUDANG','administrator','MANOP')))
def proses_ver(request):
    user =request.user
    try :
        form = forms.CharField()
        catatan = form.clean(request.POST.get('catatan',''))
    except :
        messages.add_message(request, messages.INFO,'Ada Data Yang Blm di input')
        return HttpResponseRedirect('/manop/cek_kgaktif/')
    for i in request.POST.getlist('checkeron'):
        checker = Check_Kg.objects.get(id=i)
        checker.catatan = catatan
        checker.cu =user
        checker.mu = user
        checker.status = '3'
        checker.save()
        messages.add_message(request, messages.INFO,'Verivikasi Kepala Gudang Berhasil ')
    return HttpResponseRedirect('/manop/cek_kgaktif/')

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('KEPALAGUDANG','administrator','MANOP')))
def cek_kgaktif(request):
    data = Kondisi_AktifB.objects.filter(check_kg__status= '1')
    return render(request,'manop/laporan/aktif/show_sts_kg.html',{'data':data})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('KEPALAGUDANG','administrator','MANOP')))
def cek_kredit(request,pk,object_id):
    book = get_object_or_404(AkadGadai, pk=pk)
    br = get_object_or_404(Barang ,pk =object_id)
    return render(request,'manop/laporan/aktif/partial_kredit.html',{'data':book,'barang':br})


@user_passes_test(lambda u: u.groups.filter(name__in=('KEPALAGUDANG','administrator','MANOP')))

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('STAFGUDANGAKTIF1','administrator','MANOP')))
def show_data_bap(request,pk,object_id):
    data= Barang.objects.get(id=pk)
    akad = AkadGadai.objects.get(id = object_id)
    return render(request,'manop/laporan/aktif/show_sts_aktif.html',{'data':data,'akad':akad})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('STAFGUDANGAKTIF1','administrator','MANOP')))
def data_kredit_kmr(request):
    start_date = None
    end_date = None
    form = FilterNewForm()
    if 'start_date' in request.GET and request.GET['end_date']  and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        data = AkadGadai.objects.filter(tanggal__range=(start_date,end_date))
        return render(request,'manop/laporan/aktif/data_barang_aktif.html',{'data':data,'form':form})
    return render(request,'manop/laporan/aktif/data_barang_aktif.html',{'form':form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('STAFGUDANGAKTIF1','administrator','MANOP')))
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
            status = form.cleaned_data['status']
            dus = form.cleaned_data['dus']
            tas = form.cleaned_data['tas']
            simpan =  Kondisi_AktifB(baktif= barangna,cu = user,mu =user,tanggal= datetime.date.today(),charger=charger,
                kondisi_charger=kondisi_charger,batre=batre,kondisi_batre=kondisi_batre, keybord=keybord,cassing= cassing,
                kondisi_cassing= kondisi_cassing,layar=layar,kondisi_layar=kondisi_layar,lensa=lensa,
                kondisi_lensa=kondisi_lensa,batre_kamera=batre_kamera,kondisi_batre_kamera=kondisi_batre_kamera,cassing_kamera=cassing_kamera,
                kondisi_cassing_kamera= kondisi_cassing_kamera,layar_tv=layar_tv,kondisi_layar_tv=kondisi_layar_tv,remote=remote,
                kondisi_remote=kondisi_remote,harddisk=harddisk,kondisi_harddisk=kondisi_harddisk,stick=stick,dus=dus,tas=tas,
                kondisi_stick=kondisi_stick,hdmi =hdmi,kondisi_hdmi=kondisi_hdmi,keterangan=keterangan,no_akad=pk)
            simpan.save()
            kg = Check_Kg(status = status,checker= simpan,tanggal= datetime.date.today(),cu=user,mu=user)
            kg.save()
            messages.add_message(request, messages.INFO, 'Data Penambahan Status Berhasil.')
            return HttpResponseRedirect('/manop/dlapur/data_kredit_kmr/' )
    else:
        form = DataAktifnaForm()
    return render(request,'manop/laporan/aktif/input_barang_aktif.html',{'data':data,'form':form})


