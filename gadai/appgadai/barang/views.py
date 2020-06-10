from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
from django.views.generic import create_update, list_detail
from django.template import RequestContext
from django.contrib.auth.models import User,Group
from django.shortcuts import render_to_response,get_object_or_404,render,redirect
from django import forms
from gadai.appgadai.models import *
import datetime
from gadai.appgadai.barang.form import *
from django.utils.html import escape
from django_excel_templates import *
from django_excel_templates.color_converter import *
from django.contrib.auth.decorators import login_required, user_passes_test
from gadai.appgadai.models  import *
from django.contrib import messages

def all(request, object_id):
    nsb=Nasabah.objects.get(id=object_id)
    ag=nsb.akadgadai_set.all()
    p=ag.order_by('-tanggal')
    template='barang/allnasabah.html'
    variable = RequestContext(request,{'nsb': nsb, 'ag':p})
    return render_to_response(template,variable)

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['KEPALAGUDANG','GUDANGAKTIF'])

@login_required
@user_passes_test(is_in_multiple_groups)
def rak_pusat(request, object_id,akad):
    gr = AkadGadai.objects.get(id=akad)
    user = request.user
    barang = Barang.objects.get(id=object_id)
    form = BarangGudangForm(initial={'tgl_barang_masuk': gr.tgl_barang_masuk,'agbarang': barang.id,'tgl_barang_keluar': gr.tgl_barang_keluar,\
        'lemari_barang':gr.lemari_barang,'ruang_barang':gr.ruang_barang,'row_barang':gr.row_barang,'rak_barang':gr.rak_barang,\
        'cu': user,'mu':user})    
    template = 'barang/rak_aktif.html'
    variable = RequestContext(request, {'form': form,'gr':gr,'barang':barang})
    return render_to_response(template,variable)


@login_required
@user_passes_test(is_in_multiple_groups)
def rak_input(request, object_id,akad):
    user = request.user
    gr = AkadGadai.objects.get(id=akad)
    barang = Barang.objects.get(id=object_id)
    if request.method == 'POST':
        f = BarangGudangForm(request.POST)
        if f.is_valid():
            agbarang = f.cleaned_data['agbarang']   
            tgl_barang_masuk = f.cleaned_data['tgl_barang_masuk']
            tgl_barang_keluar = f.cleaned_data['tgl_barang_keluar']
            lemari_barang = f.cleaned_data['lemari_barang']
            kolom_barang = f.cleaned_data['kolom_barang']
            rak_barang = f.cleaned_data['rak_barang']
            row_barang = f.cleaned_data['row_barang']    
            ruang_barang = f.cleaned_data['ruang_barang']                              

            f = HistoryBarang(agbarang = agbarang,tgl_barang_masuk = tgl_barang_masuk, tgl_barang_keluar = tgl_barang_keluar,\
                    lemari_barang =lemari_barang, kolom_barang = kolom_barang,rak_barang = rak_barang, row_barang = row_barang,\
                    ruang_barang = ruang_barang,cu = user,mu =user )
            f.save()

            barang.barang_masuk = tgl_barang_masuk
            barang.save()

            gr.tgl_barang_masuk=tgl_barang_masuk
            gr.tgl_barang_keluar=tgl_barang_keluar
            gr.ruang_barang = ruang_barang
            gr.lemari_barang = lemari_barang
            gr.kolom_barang = kolom_barang
            gr.row_barang = row_barang
            gr.rak_barang = rak_barang
            gr.save()                                    
            return HttpResponseRedirect('/barang/%s/all/' % gr.agnasabah.id)
    else:
        f = BarangGudangForm()
    variables = RequestContext(request, {'gr': gr, 'form': f,'barang':barang})
    return render_to_response('barang/rak_aktif.html', variables)

@login_required
@user_passes_test(is_in_multiple_groups)
def tampil_cari(request, object_id):
    gr = AkadGadai.objects.get(id=object_id)
    template='barang/cari/tampil_cari.html'  
    variables = RequestContext(request, {'gr':gr})
    return render_to_response(template,variables)

def cari_norek(request):
    rekening=request.GET['rekening']
    
    try:
        ag=AkadGadai.objects.get(id=int(rekening))
        return HttpResponseRedirect("/barang/%s/tampil_cari/" % ag.id)
    except:
        messages.add_message(request, messages.INFO,'No rekening tidak ditemukan.')
        return HttpResponseRedirect("/barang/caribarang/")


def history(request, object_id):
    barang = HistoryBarang.objects.filter(agbarang=object_id)
    variables = RequestContext(request, {'barang': barang,})
    return render_to_response('barang/historybarang.html', variables)

def rak(request,object_id):
    post = get_object_or_404(Barang, id=object_id)
    if request.method == "POST":
        form = BarangForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            h_barang = HistoryBarang(agbarang= post,tgl_barang_masuk =post.barang_masuk,tgl_barang_keluar = post.barang_keluar,\
                ruang_barang = post.ruangan,lemari_barang = post.lemari,row_barang = post.row,rak_barang = post.no_rak)
            h_barang.save()
            messages.add_message(request, messages.INFO, 'Input Posisi Barang Berhasil')
            return HttpResponseRedirect('/')
    else:
        form = BarangForm(instance=post)
    return render(request, 'barang/rak.html', {'form': form,'id':object_id}) 

def edit(request,object_id):
    coba = get_object_or_404(Barang, id=object_id)
    form = BarangForm(request.POST or None, coba=coba)
    if form.is_valid():
        form.save()
        return redirect('lanjut_view')
    return direct_to_template(request, 'edit.html', {'form': form}) 

def caribarang(request):
    akad = AkadGadai.objects.all()
    template='barang/caribarang.html'
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(template,variable)

def caribrg(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        nasabah = Nasabah.objects.filter(nama__icontains=q)
        return render_to_response('barang/namabarang.html',
            {'nasabah': nasabah, 'query': q})
    else:
        return render_to_response('/', {'error': True}) 

def tampil(request, object_id):
    barang = Barang.objects.get(id=object_id)    
    variables = RequestContext(request, {'object': barang})
    return render_to_response('barang/detail.html', variables)
    
def barang(request, object_id):
    sekarang = datetime.date.today()
    akad = AkadGadai.objects.get(id=object_id)
    form = PelunasanForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai),'gerai':akad.gerai.id,
        'jenis_barang':akad.jenis_transaksi,'terlambat':akad.hari_terlambat,'lunas':sekarang,'terlambat_kendaraan':akad.hari_terlambat,
        'jatuhtempo':akad.jatuhtempo,'bea_jasa':akad.jasa,'bea_jasa_kendaraan':akad.jasa_kendaraan})
    form.fields['pelunasan'].widget = forms.HiddenInput()
    form.fields['lunas'].widget = forms.HiddenInput()
    template = 'pelunasan/pelunasan.html'
    variable = RequestContext(request, {'akad': akad,'form': form})
    return render_to_response(template,variable)  

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['gudang','manop'])

@login_required
@user_passes_test(is_in_multiple_groups)
def xls_jatuh_tempo(request):   
    akad = AkadGadai.objects.all().filter(jatuhtempo__lte=datetime.now()).filter(perpanjang__isnull =True).filter(pelunasan__isnull=True)
    formatter = ExcelFormatter()
    simpleStyle = ExcelStyle(vert=2,wrap=1)
    formatter.addBodyStyle(simpleStyle)
    formatter.setWidth('tanggal,jatuh_tempo,nilai',3000)
    formatter.setWidth('id',500)
    formatter.setWidth('agnasabah',15000)
    formatter.setWidth('barang',20000)
    formatter.setWidth('gerai',10000)
    
    simple_report = ExcelReport()
    simple_report.addSheet("jatuhtempo")
    filter = ExcelFilter(order='id,agnasabah,gerai,barang,tanggal,jatuhtempo,nilai')
    simple_report.addQuerySet(akad,REPORT_HORZ,formatter, filter)
    
    response = HttpResponse(simple_report.writeReport(),mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=jatuh_tempo.xls'
    return response

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['gudangaktif','kepalagudang'])

@login_required
@user_passes_test(is_in_multiple_groups)
def barang_gerai(request):
    gerai = Tbl_Cabang.objects.all()
    kp = []
    for k in gerai:
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
        total_nilai_lunas +=k.plns_nilai_bulanan()
        total_lelang +=k.get_banyak_lelang()
        total_nilai_lelang += k.get_total_nilailelang()
        #total_laba_lelang +=k.get_total_labalelang()
        total_all_barang +=k.total_barang()
    
    template = 'barang/barang_gerai.html'
    variables = RequestContext(request, {
    'kp': kp ,
    'nkp' : len(kp),
    'total':total_akad,
    'tot_nilai':total_nilai,
    'tot_jatuh':total_jt,
    'tot_jt_nilai':total_jt_nilai,
    'tot_lunas':total_lunas,
    'tot_nilai_lunas':total_nilai_lunas,
    'tot_lelang':total_lelang,
    'tot_nilai_lelang':total_nilai_lelang,
    #'tot_laba_lelang':total_laba_lelang,
    'tot_all_barang':total_all_barang,
    })
    return render_to_response(template, variables)
    
@login_required
@user_passes_test(is_in_multiple_groups)
def lebih(request, object_id):
    gr = Tbl_Cabang.objects.get(id=object_id)
    ag = gr.akadgadai_set.filter(pelunasan__isnull=True)   
    template = 'barang/lebih.html'
    variables = RequestContext(request, {'gr':gr,'ag' : ag,})
    return render_to_response(template,variables)



def daftarjatuhtempo(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0]
            
    ag = AkadGadai.objects.all().filter(jatuhtempo__lte=datetime.date.today()).filter(perpanjang__isnull =True).filter(pelunasan__isnull=True)
    template = 'barang/daftarjatuhtempo.html'
    variables = RequestContext(request, {
        'tanggal':tanggal,
        'ag' : ag,
        'nilai': sum([b.nilai for b in ag ]),
        'bea_jasa': sum([b.jasa for b in ag ]),
        'bea_simpan': sum([b.biayasimpan for b in ag ]),
        'arsip_hari' : AkadGadai.objects.dates('jatuhtempo', 'day', order="DESC").filter(jatuhtempo__year=tanggal.year).filter(jatuhtempo__month=tanggal.month),
        'arsip_bulan': AkadGadai.objects.dates('jatuhtempo', 'month', order="DESC").filter(jatuhtempo__year=tanggal.year),
        'arsip_tahun' : AkadGadai.objects.dates('jatuhtempo', 'year', order="DESC"),
        'jml':len(ag),
    })
    return render_to_response(template,variables)

def cetakdaftarjatuhtempo(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0]
            
    ag = AkadGadai.objects.all().filter(jatuhtempo__lte=datetime.now()).filter(perpanjang__isnull =True).filter(pelunasan__isnull=True)
    template = 'barang/cetakdaftarjatuhtempo.html'
    variables = RequestContext(request, {
        'tanggal':tanggal,
        'ag' : ag,
        'nilai': sum([b.nilai for b in ag ]),
        'bea_jasa': sum([b.jasa for b in ag ]),
        'bea_simpan': sum([b.biayasimpan for b in ag ]),
        'arsip_hari' : AkadGadai.objects.dates('jatuhtempo', 'day', order="DESC").filter(jatuhtempo__year=tanggal.year).filter(jatuhtempo__month=tanggal.month),
        'arsip_bulan': AkadGadai.objects.dates('jatuhtempo', 'month', order="DESC").filter(jatuhtempo__year=tanggal.year),
        'arsip_tahun' : AkadGadai.objects.dates('jatuhtempo', 'year', order="DESC"),
    })
    return render_to_response(template,variables)

def jatuhtempo_harian(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('jatuhtempo', 'day', order="DESC").filter(jatuhtempo__day=tanggal.day).filter(jatuhtempo__month = tanggal.month).filter(jatuhtempo__year=tanggal.year)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('jatuhtempo', 'day', order="DESC")[0] 

    kpg =AkadGadai.objects.filter(jatuhtempo = tanggal).filter(lunas__isnull= True)
        
    template = 'barang/jatuhtempoharian.html'
    variables = RequestContext(request, {
    'kpg':kpg,
    'tanggal':tanggal,
    'nilai': sum([b.nilai for b in kpg ]),
    'bea_jasa': sum([b.tot_jasa_kend_elek for b in kpg ]),
    'bea_simpan': sum([b.tot_simpan_kend_elek for b in kpg ]),    
   
    })    
    return render_to_response(template, variables)
    
def jatuhtempo_bulanan(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('jatuhtempo', 'day', order="DESC").filter(jatuhtempo__month = tanggal.month).filter(jatuhtempo__year=tanggal.year)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('jatuhtempo', 'day', order="DESC")[0] 

    kpg = AkadGadai.objects.filter(jatuhtempo__month = tanggal.month).filter(jatuhtempo__year=tanggal.year).filter(lunas__isnull= True)
    
    template = 'barang/jatuhtempobulanan.html'
    variables = RequestContext(request, {
    'kpg':kpg, 
    'tanggal':tanggal,
    'nilai': sum([b.nilai for b in kpg ]),
    'bea_jasa': sum([b.tot_jasa_kend_elek for b in kpg ]),
    'bea_simpan': sum([b.tot_simpan_kend_elek for b in kpg ]),

    })    
    return render_to_response(template, variables)


def jatuhtempo_tahunan(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('jatuhtempo', 'day', order="DESC").filter(jatuhtempo__year=tanggal.year)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('jatuhtempo', 'day', order="DESC")[0] 

    kpg = AkadGadai.objects.filter(jatuhtempo__year=tanggal.year).filter(lunas__isnull= True)
    
    template = 'barang/jatuhtempotahunan.html'
    variables = RequestContext(request, {
    'kpg':kpg, 
    'tanggal':tanggal,
    'nilai': sum([b.nilai for b in kpg ]),
    'bea_jasa': sum([b.tot_jasa_kend_elek for b in kpg ]),
    'bea_simpan': sum([b.tot_simpan_kend_elek for b in kpg ]),    

    })    
    return render_to_response(template, variables)

def tampil(request, object_id):
    barang=Barang.objects.get(id= object_id)
    akad = barang.akadgadai_set.all()
    cari=akad.latest('id')
    variables = RequestContext(request, {'barang': barang,'cari':cari})
    return render_to_response('barang/tampil.html', variables)

###MENU POP UP
def handlePopAdd(request, BarangForm, field):
    if request.method == "POST":
        form = BarangForm(request.POST)
        if form.is_valid():
            try:
                newObject = form.save()
            except forms.ValidationError, error:
                newObject = None
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(newObject._get_pk_val()), escape(newObject)))
    else:
        form = BarangForm()

    pageContext = {'form': form, 'field': field}
    return render_to_response("barang/popadd.html", pageContext)

def newBarang(request):
    return handlePopAdd(request, BarangForm, 'barang')
###MENU POP UP

def list(request):    
    tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    return HttpResponseRedirect("/barang/arsip/?tgl=%s" % tanggal.strftime('%Y-%m-%d') )


def list_day(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []
    
    
    for (b,k) in GERAI:
        
        bn = AkadGadai.objects.filter(gerai = b ).filter(tanggal = tanggal).order_by('no').order_by('jangka_waktu')
    
        for akadgadai in bn :
            gerai.append(akadgadai)           
        
        
    template = 'barang/hari.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__year=tanggal.year).filter(tanggal__month=tanggal.month),
        'month_list': AkadGadai.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : AkadGadai.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)



def list_month(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []
    
    
    for (b,k) in GERAI:
        
        bn = AkadGadai.objects.filter(gerai = b ).filter(tanggal__month=tanggal.month).order_by('no').order_by('cu')
    
        for akadgadai in bn :
            gerai.append(akadgadai)    
           
        
        
    template = 'barang/bulan.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__year=tanggal.year).filter(tanggal__month=tanggal.month),
        'month_list': AkadGadai.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : AkadGadai.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

def list_year(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []
    
    
    for (b,k) in GERAI:
        
        bn = AkadGadai.objects.filter(gerai = b ).filter(tanggal__year=tanggal.year).order_by('no').order_by('cu')
    
        for akadgadai in bn :
            gerai.append(akadgadai)    
           
        
        
    template = 'barang/tahun.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__year=tanggal.year).filter(tanggal__month=tanggal.month),
        'month_list': AkadGadai.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : AkadGadai.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)


def status_barang(request):
    try :
        f = forms.DateField()
        barang_masuk = f.clean(request.POST.get('barang_masuk',''))
        barang_keluar = f.clean(request.POST.get('barang_keluar',''))
        
    except :
        return HttpResponseRedirect('/barang/arsip/?tgl=%s' % (request.POST.get('tgl', '')))
    for i in request.POST.getlist('id_br'):
        br = Barang.objects.get(id=int(i))
        br.barang_masuk = barang_masuk
        br.barang_keluar = barang_keluar
        
        br.save()

    return HttpResponseRedirect('/barang/arsip/?tgl=%s' % (request.POST.get('tgl', '')))


def show(request, object_id):
    gg = Tbl_Cabang.objects.get(id=object_id)
    pk=AkadGadai.objects.all()
    try:
        barang=int(request.POST['barang'])
    except:
        barang=1

    p=pk.filter(gerai=gg).filter(barang__jenis_barang=barang).order_by('-tanggal')
    variables = RequestContext(request, {'object': gg,'kredits': p,'kelompok': JENIS_BARANG,'np': len(p)})
    return render_to_response('barang/detail.html', variables)


def daftar_barang_gerai(request, object_id):
    gg = Tbl_Cabang.objects.get(id=object_id)
    pk=AkadGadai.objects.all()

    variables = RequestContext(request, {'object': gg,'kelompok': JENIS_BARANG})
    return render_to_response('barang/daftar_barang_gerai.html', variables)
###report barang aktif keseluruhan###    
def barang_aktif_gerai(request, object_id):
    gr = Tbl_Cabang.objects.get(id=object_id)
    ag = gr.akadgadai_set.filter(pelunasan__isnull=True)###barang yg belum lunas dan barang yg perpanjangan
   
    template = 'barang/barang_aktif_gerai.html'
    variables = RequestContext(request, {
        'gr':gr,
        'ag' : ag,
        'nilai': sum([b.nilai for b in ag ]),
        'bea_jasa': sum([b.jasa for b in ag ]),
        'materai': sum([b.bea_materai for b in ag ]),
        'bea_simpan': sum([b.biayasimpan for b in ag ]),
    })
    return render_to_response(template,variables)

###report barang perpanjang harian###
def barang_aktif_harian(request, object_id):
    now = datetime.date.today()
    gr = Tbl_Cabang.objects.get(id=object_id)
    ag = gr.perpanjang_set.filter(tanggal=now)  
    
    template = 'barang/barang_aktif_harian.html'
    variables = RequestContext(request, {
        'gr':gr,
        'ag' : ag,
        'nilai': sum([b.nilai for b in ag ]),
        'bea_jasa': sum([b.bea_jasa for b in ag ]),
        'denda': sum([b.denda for b in ag ]),
        'bea_simpan': sum([b.bea_simpan for b in ag ]),
    })
    return render_to_response(template,variables)

###report barang lunas keseluruhan###
def barang_lunas_gerai(request, object_id):
    gr = Tbl_Cabang.objects.get(id=object_id)
    ag = gr.pelunasan_set.filter(pelunasan__isnull=False) 
    
    template = 'barang/barang_lunas_gerai.html'
    variables = RequestContext(request, {
        'gr':gr,
        'ag' : ag,
        'nilai': sum([b.nilai for b in ag ]),
        'bea_jasa': sum([b.bea_jasa for b in ag ]),
        'denda': sum([b.denda for b in ag ]),
    })
    return render_to_response(template,variables)
    
###report barang lunas bulanan###
def barang_lunas_bulanan(request, object_id):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 

    gr = Tbl_Cabang.objects.get(id=object_id)
    ag = gr.pelunasan_set.filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year) 
    
    template = 'barang/barang_lunas_bulanan.html'
    variables = RequestContext(request, {
        'gr':gr,
        'ag' : ag,
        'nilai': sum([b.nilai for b in ag ]),
        'bea_jasa': sum([b.bea_jasa for b in ag ]),
        'denda': sum([b.denda for b in ag ]),
    })
    return render_to_response(template,variables)


###report barang lunas harian###
def barang_lunas_harian(request, object_id):
    now = datetime.date.today()
    gr = Tbl_Cabang.objects.get(id=object_id)
    ag = gr.pelunasan_set.filter(tanggal=now) 
    
    try:
        barang=int(request.POST['barang'])
    except:
        barang=1

    template = 'barang/barang_lunas_harian.html'
    variables = RequestContext(request, {
        'gr':gr,
        'ag' : ag,
        'nilai': sum([b.nilai for b in ag ]),
        'bea_jasa': sum([b.bea_jasa for b in ag ]),
        'denda': sum([b.denda for b in ag ]),
    })
    return render_to_response(template,variables)

def dafnom(request, object_id):
    tanggal = forms.DateField().clean(request.GET.get('tgl',''))
            
    barang = AkadGadai.objects.filter(gerai= str(object_id)).filter(tanggal = tanggal).order_by('gerai')
    
    template = 'barang/dafnom.html'
    variables = RequestContext(request, {
        'barang': barang,
        'tanggal' : tanggal,
        'nilai': sum([b.nilai for b in barang ]),
        'bersih' : sum([b.terima_bersih for b in barang ]),
    })    
    return render_to_response(template, variables)

def dafnom_bulan(request, object_id):    
    tanggal = forms.DateField().clean(request.GET.get('tgl',''))
            
    barang = AkadGadai.objects.filter(gerai= str(object_id)).filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year).order_by('gerai')
    template = 'barang/dafnom_bulan.html'
    variables = RequestContext(request, {
        'barang': barang,
        'tanggal' : tanggal,
        'nilai': sum([b.nilai for b in barang ]),
        'bersih' : sum([b.terima_bersih for b in barang ]),
    })    
    return render_to_response(template, variables)

def dafnom_tahun(request, object_id):    
    tanggal = forms.DateField().clean(request.GET.get('tgl',''))
            
    barang = AkadGadai.objects.filter(gerai= str(object_id)).filter(tanggal__year=tanggal.year).order_by('gerai')
    template = 'barang/dafnom_tahun.html'
    variables = RequestContext(request, {
        'barang': barang,
        'tanggal' : tanggal,
        'nilai': sum([b.nilai for b in barang ]),
        'bersih' : sum([b.terima_bersih for b in barang ]),
    })    
    return render_to_response(template, variables)
'''    
def barangnonlunas(request, object_id):
    sekarang = datetime.date.today()
    gr = Tbl_Cabang.objects.get(kode_cabang=object_id)
    ag = gr.akadgadai_set.filter(pelunasan__isnull = True).filter(jatuhtempo__lte=sekarang).exclude(status_transaksi__in = ('1','2','4','5','6','7','8','9','10')).order_by('-jatuhtempo')
    template = 'barang/barangnonlunas.html'
    variables = RequestContext(request, {
        'gr':gr,
        'ag' : ag,
        'nilai': sum([b.nilai for b in ag ]),
        'bea_jasa': sum([b.jasa for b in ag ]),
        'materai': sum([b.bea_materai for b in ag ]),
        #'bea_simpan': sum([b.biayasimpan for b in ag ]),
    })
    return render_to_response(template,variables)
'''

@login_required
def barangnonlunas(request):
    user = request.user
    start_date = None
    end_date = None
    form = NonLunasForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        ag = AkadGadai.objects.filter(gerai = user.profile.gerai,pelunasan__isnull = True,jatuhtempo__range=(start_date,end_date)).exclude(status_transaksi__in = ('1','2','4','5','6','7','8','9','10'))
        template = 'barang/barangnonlunas.html'
        variable = RequestContext(request,{ 'ag' : ag, 'nilai': sum([b.nilai for b in ag ]),
            'bea_jasa': sum([b.jasa for b in ag ]), 'materai': sum([b.bea_materai for b in ag ]),
            'start_date':start_date, 'end_date':end_date})
        return render_to_response(template,variable)
    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('barang/filter_barangnonlunas.html', variables)


