from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,render
from gadai.appgadai.gerai.views import*
from gadai.appgadai.models import *
import datetime
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.models import Tbl_Cabang,AkadGadai
from django import forms
from gadai.appgadai.templatetags.terbilang import terbilang
from django.contrib import messages
from gadai.appgadai.gerai.forms import BarangBedaForm,AKADBARANGForm,PelunasanForm,ManopForm, BarangBedaOtoForm,Filter_NeracaForm,aktifasi_userForm
D = decimal.Decimal
from django.contrib.auth.decorators import login_required

def daftar_user(request):
    us = request.user
    show = User.objects.exclude(groups__name = "NON_AKTIF").order_by('userprofile')
    variables = RequestContext(request, {'show':show})
    return render_to_response('gerai/daftar_user.html', variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='MANOP'))
def aktifkan_user(request):
    us = request.user
    show = User.objects.filter(groups__name__in =("ADM_GERAI","KASIR_GERAI")).exclude(groups__name = "NON_AKTIF").\
        exclude(userprofile__gerai_id= 1).order_by('userprofile')
    if request.method == "POST":
        form = aktifasi_userForm(request.POST)
        if form.is_valid():
            id_cabang = form.cleaned_data['id_cabang']
            kunci = User.objects.filter(userprofile__gerai =  id_cabang).filter(groups__name__in=("ADM_GERAI","KASIR_GERAI")).\
                exclude(groups__name = "NON_AKTIF")
            kunci.update(is_active = True)
            messages.add_message(request, messages.INFO, 'Buka User Berhasil')
            return HttpResponseRedirect('/')
    else:
        form  = aktifasi_userForm()
    variables = RequestContext(request, {'form': form,'show':show})
    return render_to_response('gerai/buka_user_manop.html', variables)

def keluar(request):
    usr = request.user
    usr.is_active = False
    usr.save()
    logout(request)
    return HttpResponseRedirect('/')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def status_pencairan_gerai(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    now = datetime.date.today()
    h=now.day
    m=now.month
    y=now.year
    kemarin  = now - relativedelta(days=1)
    gr = Tbl_Cabang.objects.get(kode_cabang = cab)
    ag = gr.akadgadai_set.filter(tanggal=now,jns_gu = 0)
    gu = gr.akadgadai_set.filter(tanggal=now,jns_gu = 1,lunas__isnull = True)

    akad = AkadGadai.objects.filter(tanggal = now).filter(lunas__isnull = True).filter(gerai__kode_cabang=cab).filter(jns_gu = 0)
    akad_gu = AkadGadai.objects.filter(tanggal = now).filter(lunas__isnull = True).filter(gerai__kode_cabang=cab).filter(jns_gu = 2)
    lunas = KasirGeraiPelunasan.objects.filter(tanggal =now,status = 1,kasir_lunas__gerai__kode_cabang =cab)
    lunas_kemarin= gr.pelunasan_set.filter(tanggal = now).exclude(sts_plns =2)
    return render(request,'gerai/status_pencairan_gerai.html',{'gr':gr,'ag':ag,'gu':gu,'lunas':lunas,})

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['KEPALAGUDANG','GUDANGAKTIF'])

@login_required
@user_passes_test(is_in_multiple_groups)
def filter_rekap(request):
    usr = User.objects.get(username='manop_pjb')
    nama_manop =  usr.first_name
    usr1 = User.objects.get(username='kadiv_pjb')
    nama_kadiv =  usr1.first_name
    start_date = None
    id_cabang = None
    report = None
    form = Filter_NeracaForm()
    plns = []
    
    #gr = GeraiGadai.objects.get(id = object_id)
    if 'start_date' in request.GET and request.GET['start_date'] and 'cetak' in request.GET:
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        report = request.GET['report']
        ### rincian Piutang View Gabungan
        if id_cabang != '500' and report == '1':
            plns = []
            gr = Tbl_Cabang.objects.filter(id = id_cabang)
            gerai = gr[0]
            ag = AkadGadai.objects.filter(tanggal=start_date).filter(gerai = id_cabang)
            #prpj = Perpanjang.objects.filter(tanggal=start_date).filter(gerai = id_cabang)
            lunas = Pelunasan.objects.filter(tanggal=start_date).filter(gerai = id_cabang)
            template = 'gerai/filter_pendapatan.html'
            variable = RequestContext(request, {
            'gr':gr,'ag':ag,'lunas':lunas,'nilai_pencairan': sum([b.nilai for b in ag ]),
            'jasa': sum([b.tot_jasa_kend_elek for b in ag ]),'adm': sum([b.tot_adm_kend_elek for b in ag ]),
            'simpan': sum([b.tot_simpan_kend_elek for b in ag ]),'jumlah_biaya' : sum([b.jumlah_biaya for b in ag ]),
            'terlambat': sum([b.terlambat for b in lunas ]),'denda': sum([b.denda_total for b in lunas ]),  
            'jumlah_lunas': sum ([b.tot_jasa_denda_plns for b in lunas]),
            'jasalunas': sum([b.bea_jasa_total for b in lunas]), 
            'nilai': sum ([b.nilai for b in lunas]),'nama_kadiv':nama_kadiv,'nama_manop':nama_manop,})
        return render_to_response(template,variable)
    else:
        form = Filter_NeracaForm()
        template = 'gerai/rekap_filter.html'
    variable = RequestContext(request,{'form':form})
    return render_to_response(template,variable)


def filter_neraca(request):
    #gr = GeraiGadai.objects.all()
    start_date = None
    id_cabang = None
    report = None
    form = Filter_NeracaForm()
    plns = []
    
    if 'start_date' in request.GET and request.GET['start_date'] and 'cetak' in request.GET:
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        report = request.GET['report']
        ### rincian Piutang View Gabungan
        if id_cabang != '500' and report == '1':
            plns = []
            gr = GeraiGadai.objects.filter(id = id_cabang)
            gerai = gr[0]
            ag = AkadGadai.objects.filter(tanggal=start_date).filter(gerai = id_cabang)
            prpj = Perpanjang.objects.filter(tanggal=start_date).filter(gerai = id_cabang)
            lunas = Pelunasan.objects.filter(tanggal=start_date).filter(gerai = id_cabang)
            bea = Biaya.objects.filter(tanggal=start_date).filter(gerai = id_cabang)
            template = 'gerai/rekapneraca_filter.html'

            variables = RequestContext(request, {'form':form,
      
        'saldo_bea':sum([b.saldo_awal for b in bea ]),
        'bea_pospay':sum([b.nilai_pospay for b in bea ]),
        'bea_totalkas':sum([b.jumlahkasgerai for b in bea ]),
        'bea_totalbiaya_harian' : sum([b.jumlahbiaya for b in bea ]),
        'bea_totalpengeluaran_plus_pencairan':sum([b.nilai for b in ag ]) + sum([b.jumlahbiaya for b in bea ]),
        'bea_totalkas_setoran': sum([b.jumlahkassetoran for b in bea ]),
        'bea_total_pengeluaran': sum([b.nilai for b in ag ]) + sum([b.jumlahbiaya for b in bea ]) + sum([b.jumlahkassetoran for b in bea ]),
        'bea_saldo_akhir_hari': ((sum([b.jumlahkasgerai for b in bea ]) + sum([b.saldo_awal for b in bea]) + \
            float(sum([b.nilai for b in lunas ]))) + (sum([b.jumlah_biaya for b in ag ]) + sum ([b.jasa_denda for b in lunas]))) -\
            (sum([b.nilai for b in ag ]) + sum([b.jumlahbiaya for b in bea ]) + sum([b.jumlahkassetoran for b in bea ])) + sum([b.pendapatan_lain for b in bea]),
        'jml_pospay':sum([b.jml_pospay for b in bea ]),
        'jumlah_biaya_harian_a':(sum([b.jumlahkasgerai for b in bea ]) + float(sum([b.nilai for b in lunas ]))) + \
             (sum([b.jumlah_biaya for b in ag ]) + sum ([b.jasa_denda for b in lunas])) + sum([b.saldo_awal for b in bea ]) + sum([b.pendapatan_lain for b in bea]),
        'jumlah_biaya_harian_b':(sum([b.nilai for b in ag ]) + sum([b.jumlahbiaya for b in bea ]) + \
             sum([b.saldo_awal for b in bea ]) + sum([b.jumlahkassetoran for b in bea ]))+((sum([b.jumlahkasgerai for b in bea ]) + \
             float(sum([b.nilai for b in lunas ]))) + (sum([b.jumlah_biaya for b in ag ]) + sum ([b.jasa_denda for b in lunas]))) -\
             (sum([b.nilai for b in ag ]) + sum([b.jumlahbiaya for b in bea ]) + sum([b.jumlahkassetoran for b in bea ])) + sum([b.pendapatan_lain for b in bea]),
        'prangko': sum ([b.prangko for b in bea]), 
        'surat_kilat_khusus': sum ([b.surat_kilat_khusus for b in bea]),
        'paket_pos_standar': sum([b.paket_pos_standar for b in bea]),
        'paket_kilat_khusus': sum([b.paket_kilat_khusus for b in bea]),
        'pos_express': sum([b.pos_express for b in bea]),
        'materai' : sum([b.materai for b in bea]),
        'ems' : sum([b.ems for b in bea]),
        'totalpospay': sum ([b.prangko for b in bea]) + sum ([b.surat_kilat_khusus for b in bea]) + sum([b.paket_pos_standar for b in bea])\
            + sum([b.paket_kilat_khusus for b in bea]) + sum([b.pos_express for b in bea]) + sum([b.materai for b in bea]) + sum([b.ems for b in bea]),
        'pendapatan_dll': sum([b.pendapatan_lain for b in bea]),
        'pendapatan': sum([b.pendapatan_lain for b in bea]),                 
        'gr':gr,
        'nama_cabang':gerai.nama,
        'adm_gadai':gerai.adm_gadai,
        'ag':ag,
        'total_jmlag': sum([b.nilai for b in ag ]),
        'total_jmlprpj':sum([b.nilai for b in prpj ]),
        'total_jmllunas':sum([b.nilai for b in lunas ]),

        'prpj':prpj,
        'jmllunas':len(lunas),
        'ttl_jumlah_biaya' : sum([b.jumlah_biaya for b in ag ]) + sum ([b.jasa_denda for b in lunas]),
        'ttl_pendapatan': len(lunas) + len(prpj) + len(ag),
        'lunas':lunas,
        'nilai': sum([b.nilai for b in ag ]),
        'jasa': sum([b.tot_jasa_kend_elek for b in ag ]),
        'adm': sum([b.tot_adm_kend_elek for b in ag ]),
        'simpan': sum([b.tot_simpan_kend_elek for b in ag ]),
        'jumlah_biaya' : sum([b.jumlah_biaya for b in ag ]),
        'simpanprpj': sum([b.bea_simpan_total for b in prpj ]),
        'jasaprpj': sum([b.bea_jasa_total for b in prpj ]),
        'dendaprpj': sum([b.denda_total for b in prpj ]), 
        'jumlahbiaya': sum([b.pndptan_prpj_total for b in prpj ]),  
        'terlambat': sum([b.terlambat for b in lunas ]),  
        'denda': sum([b.denda_total for b in lunas ]),  
        'jumlah_lunas': sum ([b.jumlah_pelunasan for b in lunas]), 
        'nilai': sum ([b.nilai for b in lunas]),
        'bea_jasa': sum ([b.bea_jasa_total for b in lunas]),
        'jumlahjasa_lunas': sum ([b.jasa_denda for b in lunas]),
        'tunai_pusat' : sum ([b.tunai for b in bea]),
        'bank' : sum ([b.bank for b in bea]), 
        'dari_gerai':sum([b.dari_gerai for b in bea]),
        #'jml_pospay':sum([b.jml_pospay for b in bea]),

        'pln': sum([b.listrik for b in bea]),
        'pdam':sum([b.pdam for b in bea]),
        'tlp':sum([b.telpon for b in bea]),
        'foto_copy':sum([b.foto_copy for b in bea]),
        'majalah':sum([b.majalah for b in bea]),
        'keamanan':sum([b.iuran_keamanan for b in bea]),
        'kebersihan':sum([b.iuran_kebersihan for b in bea]),
        'promosi':sum([b.promosi for b in bea]),
        'air_minum':sum([b.air_minum for b in bea]),
        'sewa':sum([b.sewa_gedung_gerai for b in bea]),
        'setoran_bank':sum([b.setoran_bank for b in bea]),
        'tunai':sum([b.tunai_pickup for b in bea]),
        'kegerai':sum([b.ke_gerai for b in bea]),
        'start_date':start_date,
        
            })
            return render_to_response(template, variables)
    else:
        form = Filter_NeracaForm()
        template = 'gerai/neraca_baru.html'
    variable = RequestContext(request,{'form':form})
    return render_to_response(template,variable)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def plan_jatuh_tempo_gerai(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    rekap = Tbl_Cabang.objects.get(kode_cabang=cab)
    plns = []
    sekarang = datetime.date.today()
    aa = rekap.akadgadai_set.filter(jatuhtempo=sekarang).filter(lunas__isnull = True)
    all_pk_lunas = Pelunasan.objects.filter(tanggal=sekarang)
    all_pk_akad  = AkadGadai.objects.filter(tanggal=sekarang)
    template = 'manop/filter/plan_jatuh_tempo_gerai.html'
    variables = RequestContext(request, {'rekap':rekap,
            'aa': aa ,'total_noa_jt' : aa.count(),
            'total_nilai_jt':sum([p.nilai for p in aa]),
            'total_nilai_plan_jt': sum([p.nilai for p in aa]) * 0.008,})
    return render_to_response(template,variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def status_barang_gerai(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    gr = Tbl_Cabang.objects.get(kode_cabang = cab)
    start_date = datetime.date(2015,03,18)
    end_date = datetime.date.today()
    gerai = gr.akadgadai_set.filter(sts_tdr__isnull = True,tanggal_permintaan__range =(start_date,end_date),status_permintaan__in=('3')).exclude(sts_tdr = 1)
    template = 'gerai/status/status_barang_gerai.html'
    variables = RequestContext(request, {'gr':gr,'total':len(gerai),'gerai':gerai,
        'nilai': sum([b.terima_bersih for b in gerai ]),})
    return render_to_response(template,variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def cetak_status_barang(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    gr = Tbl_Cabang.objects.get(kode_cabang = cab)
    start_date = datetime.date(2015,03,18)
    end_date = datetime.date.today()
    gerai = gr.akadgadai_set.filter(sts_tdr__isnull = True,tanggal_permintaan__range =(start_date,end_date),status_permintaan__in=('3'))
    template = 'gerai/status/cetak_status_barang.html'
    variables = RequestContext(request, {'gr':gr,'total':len(gerai),'gerai':gerai,'end_date':end_date,})
    return render_to_response(template,variables)

@login_required
def batal_lunas_barangsama(request, object_id,barang,taksir):
    user = request.user
    sekarang = datetime.date.today()
    ag = AkadGadai.objects.get(id=object_id)
    loglunas = LogPelunasan(norek=ag.id,tanggal =sekarang,nilai = ag.nilai,gerai = ag.gerai.nama_cabang,\
        status ='pelunasan gu',cu =user,mu=user)     
    loglunas.save()
    ag.lunas = None
    ag.status_transaksi = None
    ag.status_kwlunas = None
    ag.save()
    tbl_pelunasan = ag.pelunasan_set.all()
    tbl_pelunasan.delete()       
    id_akad = ag.id
    messages.add_message(request, messages.INFO, 'Batal Gadai Ulang Barang sama')
    return HttpResponseRedirect(ag.get_nasabah_url())

@login_required
def barang_beda(request, object_id):
    nsb = Nasabah.objects.get(id = object_id)
    searang = datetime.date.today()
    form = AKADBARANGForm(initial={'agnasabah': nsb.id,'gerai':nsb.geraigadai,'tanggal':searang})
    form.fields['agnasabah'].widget = forms.HiddenInput()
    template = 'gerai/add/input_barang_beda.html'
    variables = RequestContext(request, {'object':nsb,'form':form})
    return render_to_response(template,variables)

@login_required
def baru_beda_barang(request):
    request.user
    #nsb = Nasabah.objects.get(id = object_id)
    if request.method == "POST":
        form = AKADBARANGForm(request.POST, request.FILES)
        if form.is_valid():
            agnasabah = form.cleaned_data['agnasabah']
            tanggal = form.cleaned_data['tanggal']
            gerai = form.cleaned_data['gerai']
            taksir = form.cleaned_data['taksir'] 
            nilai = form.cleaned_data['nilai']            
            bea_materai = form.cleaned_data['bea_materai']
            jenis_transaksi = form.cleaned_data['jenis_transaksi']
            pilih_jasa = form.cleaned_data['pilih_jasa']

            jangka_waktu = form.cleaned_data['jangka_waktu']
            jangka_waktu_kendaraan = form.cleaned_data['jangka_waktu_kendaraan'] 
            jenis_kendaraan = form.cleaned_data['jenis_kendaraan']
            jenis_barang = form.cleaned_data['jenis_barang']
            
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
            
            password = form.cleaned_data['password']
            password_barang = form.cleaned_data['password_barang']            
            optik_ps = form.cleaned_data['optik_ps']
            kondisi_optik_ps = form.cleaned_data['kondisi_optik_ps']            
            harddisk  = form.cleaned_data['harddisk']
            kondisi_harddisk = form.cleaned_data['kondisi_harddisk']
            stick  = form.cleaned_data['stick']
            kondisi_stick = form.cleaned_data['kondisi_stick']
            hdmi  = form.cleaned_data['hdmi']
            kondisi_hdmi = form.cleaned_data['kondisi_hdmi']
            remote = form.cleaned_data['remote']
            kondisi_remote = form.cleaned_data['kondisi_remote']
            dus = form.cleaned_data['dus']
            tas = form.cleaned_data['tas']
            layar_tv = form.cleaned_data['layar_tv']
            kondisi_layar_tv = form.cleaned_data['kondisi_layar_tv']
            accesoris_barang1 = form.cleaned_data['accesoris_barang1']
            bpkb = form.cleaned_data['bpkb']
            stnk = form.cleaned_data['stnk']
            faktur = form.cleaned_data['faktur']
            gesek_nomesin = form.cleaned_data['gesek_nomesin']
            gesek_norangka = form.cleaned_data['gesek_norangka']
            sn= form.cleaned_data['sn']
            warna = form.cleaned_data['warna']
            tahun_pembuatan =form.cleaned_data['tahun_pembuatan']
            bulan_produksi = form.cleaned_data['bulan_produksi']
            lampiran_dokumen = form.cleaned_data['lampiran_dokumen']  
            merk_kendaraan = form.cleaned_data['merk_kendaraan']
            type_kendaraan = form.cleaned_data['type_kendaraan']
            tahun_pembuatan_kendaraan = form.cleaned_data['type_kendaraan']
            no_polisi = form.cleaned_data['no_polisi']
            no_rangka = form.cleaned_data['no_rangka']
            no_mesin = form.cleaned_data['no_mesin']
            warna_kendaraan = form.cleaned_data['warna_kendaraan']
            no_bpkb = form.cleaned_data['no_bpkb']
            stnk_atas_nama = form.cleaned_data['stnk_atas_nama']
            no_faktur = form.cleaned_data['no_faktur']
            jasa_baru = form.cleaned_data['jasa_baru']
            beasimpan_baru = form.cleaned_data['beasimpan_baru']
            adm_baru = form.cleaned_data['adm_baru']
            total_all = form.cleaned_data['total_all']
            
            tanda_tangan = form.cleaned_data['tanda_tangan']
            foto_nasabah = form.cleaned_data['foto_nasabah']
            berkas_barang = form.cleaned_data['berkas_barang']
            
            barang = Barang(sn=sn,warna=warna,tahun_pembuatan=tahun_pembuatan,bulan_produksi=bulan_produksi,
                lampiran_dokumen=lampiran_dokumen,accesoris_barang1=accesoris_barang1,jenis_barang=jenis_barang,
                merk_kendaraan=merk_kendaraan,no_polisi=no_polisi,no_rangka=no_rangka,no_mesin=no_mesin,warna_kendaraan=warna_kendaraan,
                no_bpkb=no_bpkb,stnk_atas_nama=stnk_atas_nama,no_faktur=no_faktur,jenis_kendaraan=jenis_kendaraan,
                type_kendaraan=type_kendaraan,\
                charger=charger,kondisi_charger=kondisi_charger,batre=batre,kondisi_batre=kondisi_batre,keybord=keybord,
                kondisi_keybord=kondisi_keybord,cassing=cassing,kondisi_cassing = kondisi_cassing,layar=layar,
                kondisi_layar=kondisi_layar,lensa=lensa,kondisi_lensa=kondisi_lensa,optik_ps=optik_ps,kondisi_optik_ps=kondisi_optik_ps,
                bpkb=bpkb,stnk=stnk,faktur=faktur,gesek_nomesin=gesek_nomesin,gesek_norangka=gesek_norangka,
                layar_tv=layar_tv,kondisi_layar_tv = kondisi_layar_tv,
                harddisk = harddisk,kondisi_harddisk = kondisi_harddisk,stick  = stick,kondisi_stick = kondisi_stick,hdmi  = hdmi,kondisi_hdmi = kondisi_hdmi,
                remote = remote,kondisi_remote = kondisi_remote,dus = dus,tas = tas,
                batre_kamera = batre_kamera,kondisi_batre_kamera = kondisi_batre_kamera,cassing_kamera = cassing_kamera,
                kondisi_cassing_kamera = kondisi_cassing_kamera,password = password,password_barang =password_barang,akad_ulang=0,
                buka_tutup_gu =99)
            barang.save()

            if barang.jenis_barang == u'':
                barang.jenis_barang = u'0'
                barang.save()
            if barang.jenis_kendaraan == u'':
                barang.jenis_barang = u'0'
                barang.save()
            
            akad = AkadGadai (tanggal = tanggal,agnasabah=agnasabah, gerai=gerai, jangka_waktu=jangka_waktu,
                nilai=nilai,cu=request.user, mu=request.user,taksir=taksir,barang=barang,
                bea_materai=bea_materai, jangka_waktu_kendaraan=jangka_waktu_kendaraan,jns_gu = 0,
                jenis_transaksi=jenis_transaksi)
            if akad.jenis_transaksi != u'1':
                    akad.pilih_jasa = int(pilih_jasa)
                    akad.save()
            '''    
            '''
            if  akad.jenis_transaksi == u'1' and akad.nilai > akad.taksir.maxpinjaman and akad.agnasabah.jenis_keanggotaan == u'1':
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.status_kw = 0
                akad.status_label = 0
                akad.jns_gu = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                akad.save()
                
            elif akad.jenis_transaksi == u'2' and akad.nilai > akad.taksir.maxpinjaman and akad.agnasabah.jenis_keanggotaan == u'1':
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.status_kw = 0
                akad.status_label = 0
                akad.jns_gu = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                akad.save()
                
            elif akad.jenis_transaksi == u'1' and akad.nilai <=  akad.taksir.maxpinjaman and akad.agnasabah.jenis_keanggotaan == u'1':
                akad.status_taksir = 1
                akad.asumsi_jasa = akad.asumsi_pendapatan_jasa()
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.status_kw = 0
                akad.status_label = 0
                akad.jns_gu = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()

            elif akad.jenis_transaksi == u'2' and akad.nilai <= akad.taksir.maxpinjaman and akad.agnasabah.jenis_keanggotaan == u'1':
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.status_kw = 0
                akad.status_label = 0
                akad.jns_gu = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()

            elif  akad.jenis_transaksi == u'1' and akad.nilai > akad.taksir.maxpinjaman and akad.agnasabah.jenis_keanggotaan == u'2':
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.status_kw = 0
                akad.status_label = 0
                akad.jns_gu = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                akad.save()
                
            elif akad.jenis_transaksi == u'2' and akad.nilai > akad.taksir.maxpinjaman and akad.agnasabah.jenis_keanggotaan == u'2':
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.status_kw = 0
                akad.status_label = 0
                akad.jns_gu = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                akad.save()

            elif akad.jenis_transaksi == u'1' and akad.nilai <=  akad.taksir.maxpinjaman and akad.agnasabah.jenis_keanggotaan == u'2':
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.status_kw = 0
                akad.status_label = 0
                akad.jns_gu = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
            #elif ag.jenis_transaksi == u'2' and ag.nilai <= ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
            else:
                akad.status_taksir = 1
                akad.asumsi_jasa = akad.asumsi_pendapatan_jasa()
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.status_kw = 0
                akad.status_label = 0
                akad.jns_gu = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
            brg = Barang.objects.all()
            banding = brg.filter(id = akad.barang_id)
            print banding
            banding.update(merk = akad.taksir.type,type = akad.taksir.type ) 
            request.FILES['tanda_tangan'].name = akad.agnasabah.nama + '_' +  akad.norek() + '_' + request.FILES['tanda_tangan'].name
            request.FILES['foto_nasabah'].name = akad.agnasabah.nama + '_' +  akad.norek() + '_' + request.FILES['foto_nasabah'].name
            request.FILES['berkas_barang'].name = akad.agnasabah.nama + '_' + akad.norek() + '_' + request.FILES['berkas_barang'].name
            berkas = BerkasGadai(upload=akad, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                berkas_barang=request.FILES['berkas_barang'])
            berkas.save()
            return HttpResponseRedirect('/')
    else:
        form = AKADBARANGForm()
        form.fields['pilih_jasa'].widget = forms.HiddenInput()
    template='gerai/add/input_barang_beda.html'
    variable = RequestContext(request, {'form':form})
    return render_to_response(template,variable)

def jurnal_pencairan(akad, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_pinjaman = get_object_or_404(Tbl_Akun, id=163L)
    a_pdp_adm = get_object_or_404(Tbl_Akun, id='430')
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='383')
    a_pdp_bea_simpan = get_object_or_404(Tbl_Akun, id='429')
    a_pdp_bea_materai = get_object_or_404(Tbl_Akun, id='608')
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),tgl_trans =akad.tanggal,nobukti=akad.norek(),
        object_id=ag.norek_id())
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = akad.nilai,kredit = 0,
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,
        id_unit= 300)
    
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_adm,
        debet = 0,kredit = D(float(akad.adm_all())),
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,
        id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_bea_materai,
        debet = 0,kredit = D(float(akad.bea_materai)),
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,
        id_unit= 300)

    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,no_trans = no_trans,
        debet = 0,kredit =  D(float(akad.jasa_all())),
        id_product = '4',status_jurnal ='1',
        id_cabang = akad.gerai.kode_cabang,tgl_trans =akad.tanggal,id_unit= 300)

    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit =  D(float(akad.beasimpan_all())),
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        debet = 0 ,  kredit = round(D(akad.nilai) - D(akad.adm_all()) - akad.jasa_all() - akad.beasimpan_all()),
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,
        id_unit= 300)

def jurnal_pencairan_nonanggota(akad, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_pinjaman = get_object_or_404(Tbl_Akun, id=166L)
    a_pdp_adm = get_object_or_404(Tbl_Akun, id='432')
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='383')
    a_pdp_bea_simpan = get_object_or_404(Tbl_Akun, id='429')
    a_pdp_bea_materai = get_object_or_404(Tbl_Akun, id='608')
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),tgl_trans =akad.tanggal,nobukti=akad.norek(),
        object_id=akad.norek_id())
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = akad.nilai,kredit = 0,
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_adm,
        debet = 0,kredit = D(float(akad.adm_all())),
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,
        debet = 0,kredit =  D(float(akad.jasa_all())),
        id_product = '4',status_jurnal ='1',
        id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_bea_materai,
        debet = 0,kredit = D(float(akad.bea_materai)),
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit =  D(float(akad.beasimpan_all())),
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        debet = 0 , kredit = round(D(akad.nilai) - D(akad.adm_all()) - akad.jasa_all() - akad.beasimpan_all()),#D(ag.jasa_all()) 
        id_product = '4',status_jurnal ='1',id_cabang =akad.gerai.kode_cabang,tgl_trans =akad.tanggal,
        id_unit= 300)

@login_required
def pelunasan_gu_sbl(request,object_id):
    nas = Pelunasan.objects.get(id=object_id)
    akad = AkadGadai.objects.get(id = nas.pelunasan.id)
    if request.method == "POST":
        form = ManopForm(request.POST)
        if form.is_valid():
            tanggal_manop = form.cleaned_data['tanggal_manop']
            comment = form.cleaned_data['comment']
            manopgu = ManopPelunasanGu(gu = nas,tanggal =tanggal_manop,note=comment,status=1)
            manopgu.save()
            akad.status_oto_akad_gu = 1
            akad.save()
            messages.add_message(request, messages.INFO, 'Otorisasi Manop Pelunasan')
            return HttpResponseRedirect(akad.get_nasabah_url())
    else:
        form = ManopForm()        
    return render(request, 'gerai/add/edit_pelunasan_gu.html', {'form': form,'id':nas})

@login_required
def barang_sama_oto_manop(request, object_id,barang,taksir):
    searang = datetime.date.today()
    nsb = Nasabah.objects.get(id = object_id)
    taksir1 = Taksir.objects.get(id=taksir)
    barang1 = Barang.objects.get(id=barang)
    cek = nsb.akadgadai_set.filter(taksir = taksir1).filter(barang = barang1)#.filter(lunas__isnull = True)
    ag = cek[0]
    plns = Pelunasan.objects.get(pelunasan=ag.id)  
    akad = AkadGadai.objects.get(id = ag.id)
    akad.status_oto_akad_gu = 3#### UNTUK MENGHILANGKAN TOMBOL OTORISASI GU  
    akad.save()
    form = BarangBedaOtoForm(initial={'agnasabah': nsb.id,'gerai':nsb.geraigadai,'barang':barang,'taksir':taksir,'tanggal':searang,\
        'jenis_transaksi':ag.jenis_transaksi,'jenis_barang':nsb.jenis_barang,'sn':nsb.sn,'nilai_gu':int(plns.nilai),
        'denda_gu':int(plns.denda) + int(plns.denda_kendaraan),
        'pokok':int(plns.nilai),'denda':int(plns.denda) + int(plns.denda_kendaraan),
        'denda_keterlambatan': int(plns.bea_jasa) +  int(plns.bea_jasa_kendaraan),'batre':(barang1.batre),\
        'kewajiban_pelunasan' :(int(plns.nilai) + int(plns.denda) + int(plns.denda_kendaraan)) + \
        int(plns.bea_jasa) +  int(plns.bea_jasa_kendaraan),
        'jasa_gu':int(plns.bea_jasa_kendaraan) + int(plns.bea_jasa)})
    form.fields['agnasabah'].widget = forms.HiddenInput()
    form.fields['denda_gu'].widget = forms.HiddenInput()
    form.fields['nilai_gu'].widget = forms.HiddenInput()
    form.fields['jasa_gu'].widget = forms.HiddenInput()
    form.fields['barang'].widget = forms.HiddenInput()
    template = 'gerai/add/input_barang_sama_oto_manop.html'
    variables = RequestContext(request, {'object':nsb,'form':form,'ag':ag,'plns':plns})
    return render_to_response(template,variables)

@login_required
def barang_sama(request, object_id,barang,taksir):
    searang = datetime.date.today()
    nsb = Nasabah.objects.get(id = object_id)
    #ag = nsb.akadgadai_set.all().latest()
    taksir1 = Taksir.objects.get(id=taksir)
    barang1 = Barang.objects.get(id=barang)
    cek = nsb.akadgadai_set.filter(taksir = taksir1).filter(barang = barang1).filter(lunas__isnull = True)
    ag = cek[0]
    ag.status_transaksi = 1
    ag.lunas = searang
    ag.status_kwlunas = 0
    ag.status_mcc = 0
    ag.status_kw = 0
    ag.jns_gu = 1
    ag.norek_lunas_sblm = ag.norek()
    ag.save()

    plns=Pelunasan(nilai=ag.nilai,tanggal=searang,denda = int(ag.denda_elektronik()),bea_jasa=int(ag.hitung_jasa_pelunasan_elektronik()),\
        pelunasan_id=ag.id,denda_kendaraan=int(ag.denda_kendaraan()),val= 0,bea_jasa_kendaraan=int(ag.hitung_jasa_pelunasan_kendaraan()),\
        status_pelunasan =1,jenis_barang = ag.jenis_transaksi,gerai=ag.gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
        status=1,sts_plns= 2)
    plns.save()

    form = BarangBedaForm(initial={'agnasabah': nsb.id,'gerai':nsb.geraigadai,'barang':barang,'taksir':taksir,'tanggal':searang,\
        'jenis_transaksi':ag.jenis_transaksi,'jenis_barang':nsb.jenis_barang,'sn':nsb.sn,'nilai_gu':int(plns.nilai),
        'denda_gu':int(plns.denda) + int(plns.denda_kendaraan),'pokok':int(plns.nilai),'denda':int(ag.denda_all_transaksi()),
        'denda_keterlambatan': int(ag.hitung_jasa_pelunasan()),
        'kondisi_batre':(barang1.kondisi_batre ),
        'charger':(barang1.charger),'kondisi_charger':(barang1.kondisi_charger),'keybord':(barang1.keybord),\
        'kondisi_keybord':(barang1.kondisi_keybord),'password':(barang1.password),'password_barang':(barang1.password_barang),\
        'cassing':(barang1.cassing),'kondisi_cassing':(barang1.kondisi_cassing),\
        'layar':(barang1.layar),'kondisi_layar':(barang1.kondisi_layar),'dus':(barang1.dus),'tas':(barang1.tas),\
        'optik_ps':(barang1.kondisi_optik_ps),'harddisk':(barang1.harddisk),'stick':(barang1.stick),\
        'kondisi_stick':(barang1.kondisi_stick),'hdmi':(barang1.hdmi),'kondisi_hdmi':(barang1.kondisi_hdmi),\
        'layar_tv':(barang1.layar_tv),'kondisi_layar_tv':(barang1.kondisi_layar_tv),'remote':(barang1.kondisi_remote),\
        'bpkb':(barang1.bpkb),'stnk':(barang1.stnk),'faktur':(barang1.faktur),'gesek_nomesin':(barang1.gesek_nomesin),\
        'gesek_norangka':(barang1.gesek_norangka),\
        'kewajiban_pelunasan' :(int(ag.nilai) + int(ag.denda_elektronik()) + int(ag.hitung_jasa_pelunasan_elektronik()) + \
        int(ag.denda_kendaraan()) + int(ag.hitung_jasa_pelunasan_kendaraan())),
        'jasa_gu':int(plns.bea_jasa_kendaraan) + int(plns.bea_jasa)})
    form_oto= ManopForm(initial={'tanggal':searang})
    form.fields['agnasabah'].widget = forms.HiddenInput()
    form.fields['denda_gu'].widget = forms.HiddenInput()
    form.fields['nilai_gu'].widget = forms.HiddenInput()
    form.fields['jasa_gu'].widget = forms.HiddenInput()
    form.fields['barang'].widget = forms.HiddenInput()
    template = 'gerai/add/input_barang_sama.html'
    variables = RequestContext(request, {'object':nsb,'form':form,'ag':ag,'form_oto':form_oto,'plns':plns})
    return render_to_response(template,variables)


def baru(request):
    user = request.user
    D = decimal.Decimal
    sekarang = datetime.date.today()
    if request.method == "POST":
        form = BarangBedaForm(request.POST)
        if form.is_valid():
            agnasabah = form.cleaned_data['agnasabah']
            tanggal = form.cleaned_data['tanggal']
            gerai = form.cleaned_data['gerai']
            jenis_transaksi = form.cleaned_data['jenis_transaksi']
            pilih_jasa = form.cleaned_data['pilih_jasa']

            taksir = form.cleaned_data['taksir'] 
            jangka_waktu = form.cleaned_data['jangka_waktu']
            nilai = form.cleaned_data['nilai']
            jenis_kendaraan = form.cleaned_data['jenis_kendaraan']
            barang = form.cleaned_data['barang']
            jangka_waktu_kendaraan = form.cleaned_data['jangka_waktu_kendaraan']
            bea_materai = form.cleaned_data['bea_materai']
            jenis_barang = form.cleaned_data['jenis_barang']   
    ###new input 1 april
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
            password = form.cleaned_data['password']
            password_barang = form.cleaned_data['password_barang']            
            
            lensa = form.cleaned_data['lensa']
            kondisi_lensa = form.cleaned_data['kondisi_lensa']
            batre_kamera = form.cleaned_data['batre_kamera']
            kondisi_batre_kamera = form.cleaned_data['kondisi_batre_kamera']
            cassing_kamera = form.cleaned_data['cassing_kamera']
            kondisi_cassing_kamera = form.cleaned_data['kondisi_cassing_kamera']
            
            optik_ps = form.cleaned_data['optik_ps']
            kondisi_optik_ps = form.cleaned_data['kondisi_optik_ps']
            harddisk  = form.cleaned_data['harddisk']
            kondisi_harddisk = form.cleaned_data['kondisi_harddisk']
            stick  = form.cleaned_data['stick']
            kondisi_stick = form.cleaned_data['kondisi_stick']
            hdmi  = form.cleaned_data['hdmi']
            kondisi_hdmi = form.cleaned_data['kondisi_hdmi']
            remote = form.cleaned_data['remote']
            kondisi_remote = form.cleaned_data['kondisi_remote']
            dus = form.cleaned_data['dus']
            tas = form.cleaned_data['tas']
            accesoris_barang1 = form.cleaned_data['accesoris_barang1']
            bpkb = form.cleaned_data['bpkb']
            stnk = form.cleaned_data['stnk']
            faktur = form.cleaned_data['faktur']
            gesek_nomesin = form.cleaned_data['gesek_nomesin']
            gesek_norangka = form.cleaned_data['gesek_norangka']
            kewajiban_pelunasan = form.cleaned_data['kewajiban_pelunasan']
            nilai_gu = form.cleaned_data['nilai_gu']
            jasa_gu = form.cleaned_data['jasa_gu']   
            denda_gu = form.cleaned_data['denda_gu']
            pokok = form.cleaned_data['pokok']
            denda = form.cleaned_data['denda']
            denda_keterlambatan = form.cleaned_data['denda_keterlambatan']

            jasa_baru = form.cleaned_data['jasa_baru']
            beasimpan_baru = form.cleaned_data['beasimpan_baru']
            adm_baru = form.cleaned_data['adm_baru']
            kewajiban_total_baru = form.cleaned_data['kewajiban_total_baru']
            total_all = form.cleaned_data['total_all']
            
            akad = AkadGadai (tanggal = tanggal,agnasabah=agnasabah, gerai=gerai, jangka_waktu=jangka_waktu,
                nilai=nilai,cu=request.user, mu=request.user,taksir=taksir,barang=barang,
                bea_materai=bea_materai, jangka_waktu_kendaraan=jangka_waktu_kendaraan,
                nilai_gu=nilai_gu,denda_gu=denda_gu,jasa_gu =jasa_gu,total_plns_gu=total_all,
                jenis_transaksi=jenis_transaksi,kewajiban_pelunasan = kewajiban_pelunasan,status_kw = '0')
            akad.save()
            a = akad.agnasabah.akadgadai_set.filter(lunas__isnull = False)
            b = a.latest()
            akad.norek_lunas_sblm = b.norek()
            akad.save()
            if akad.jenis_transaksi != u'1':
                    akad.pilih_jasa = int(pilih_jasa)
                    akad.save()            
            user = request.user
            #aa = b.berkasgadai_set.all()
            #bb = aa[0]
            #berkas = BerkasGadai(upload = akad, tanda_tangan = bb.tanda_tangan, foto_nasabah = bb.foto_nasabah, berkas_barang = bb.berkas_barang)
            #berkas.save()

            ###111
            if  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()                
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')                 
                jurnal_akad_barang_sama_anggota(akad, user)###Jurnal pencairan baru
                jurnal_pelunasan_barang_sama_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Denda 1(617)')

            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0 and akad.jasa_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Materai NonDenda 8 (1489)(11)')
 
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()                
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')                 
                jurnal_akad_barang_sama_anggota(akad,request.user)###Jurnal pencairan baru
                jurnal_pelunasan_barang_sama_anggota_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai NonDenda1 (633)')
            ###222
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()                
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')                 
                jurnal_akad_barang_sama_anggota(akad, request.user)
                jurnal_pelunasan_barang_sama_anggota_lebih(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Denda 2(651)')
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota_lebih_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Non Denda 2(668)')
            ###333
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()                 
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')                 
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota_lebih(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Denda 3(686)')
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota_lebih_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Non Denda (703)')
            ###444
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()               
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')                 
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Denda (721)')
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Denda(738)')
            ###555
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()               
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')                 
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota_lebih(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai(756)')
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota_lebih_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai(773)')
            ###666
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()                
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')                 
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Mataerai denda(791)')
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Mataerai Nondenda(808)')
            ###777
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()               
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')                 
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Denda(826)')
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota(akad, user)
                jurnal_pelunasan_barang_sama_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Nondenda (843)')
            
            ###taksiran
            ####888
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0 and akad.jasa_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_non_denda_terlambat(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Denda 8 (858)')


            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0 and akad.jasa_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Denda 8 (877)') 
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0 and akad.jasa_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_non_denda_oto(akad, user)
                #jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Nondenda 8 (894)')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0 and akad.jasa_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad, user)
                #jurnal_pelunasan_barang_sama_non_anggota_non_denda_oto(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Nondenda 8 (911)')

            ###999
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai Denda(937)') 
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Non Materai NonDenda(954)')

            ####10
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_anggota(akad, request.user)
                jurnal_pelunasan_barang_sama_anggota_lebih(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting Dengan Baik Non Materai DEnda (973)') 
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_anggota(akad, request.user)
                jurnal_pelunasan_barang_sama_anggota_lebih_nondenda(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting Dengan Baik Non Materai Non Denda(990)')

            ####11
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Non Materai Denda(1009)')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Non Materai Non Denda(1026)')

            ####12
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik nOn Materai Denda(1045)') 
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu ==0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik nOn Materai Non Denda(1062)')
            ####13
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik non Materai Denda(1080)')  
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu ==0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik non Materai Nondenda(1097)')

            ####14
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Non Materai denda(1116)')  
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Non Materai Non Denda(1133)')

            ###15
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Non Materai denda(1152)')  
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Non Materai nondenda(1169)')
            ###16
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Non Materai Denda(1187)')  
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai == 0 and akad.denda_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota(akad, user)
                jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Non Materai nondenda(1204)')
            #####materai bro
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)###Jurnal pencairan baru
                jurnal_pelunasan_barang_sama_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik MATERAI Denda (1222)')
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)###Jurnal pencairan baru
                jurnal_pelunasan_barang_sama_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik MATERAI NonDenda 1239')

            ###222
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)
                jurnal_pelunasan_barang_sama_anggota_lebih(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik MATERAI Denda 1258')
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)
                jurnal_pelunasan_barang_sama_anggota_lebih_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik MATERAI NonDenda 1275')
            ###444
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.gadai_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)
                jurnal_pelunasan_barang_sama_anggota(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik MATERAI Denda 1293')
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai > akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.gadai_gu ==0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)
                jurnal_pelunasan_barang_sama_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik MATERAI Nondenda 1310')
            ###555
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)
                jurnal_pelunasan_barang_sama_anggota_lebih(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik MATERAI Denda 1328')
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)
                jurnal_pelunasan_barang_sama_anggota_lebih_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik MATERAI Nondenda 1345')

            ###666
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0 and akad.jasa_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota(akad, request.user)
                #jurnal_pelunasan_barang_sama_anggota(akad, request.user)
                jurnal_pelunasan_barang_sama_anggota_non_denda_terlambat(akad,request.user) ##### 4 februari
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik  MATERAI Denda 1364 (14)')
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                #messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)
                #jurnal_akad_barang_sama_anggota(akad, request.user)
                jurnal_pelunasan_barang_sama_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik  MATERAI NonDenda 6 (1381)')
            ###777
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, request.user)
                jurnal_pelunasan_barang_sama_anggota(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Materai Denda 1400')
            elif  akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1' and \
                akad.nilai <= akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                jurnal_akad_barang_sama_anggota_materai(akad, user)
                jurnal_pelunasan_barang_sama_anggota_nondenda(akad, user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Materai 1417')

            ###888 Denda
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0 and akad.jasa_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_anggota_non_denda_terlambat(akad,request.user)
                #jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad, request.user)


            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad, request.user)
                jurnal_pelunasan_barang_sama_non_anggota(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Materai Denda 8 (1435)')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0 and akad.jasa_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota_materai(akad, request.user)
                jurnal_pelunasan_barang_sama_non_anggota_non_denda_oto(akad, request.user)
                #jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Materai NonDenda 8 (1447)')
            #'''sepur123
            #elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                #and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0 and akad.jasa_gu == 0:
                #akad.status_taksir = 1
                #akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                #akad.os_pokok = akad.nilai
                #akad.jatuhtempo = akad.menu_hitung_jt()
                #akad.nilai_adm = D(akad.adm)
                #akad.nilai_jasa = D(round(akad.jasa))
                #akad.nilai_biayasimpan = D(akad.biayasimpan)
                #akad.nilai_asuransi = 0
                #akad.nilai_provisi = 0
                #akad.jns_gu = 1
                #akad.save()
                #messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                #jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                #jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad,request.user)
                #messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Materai NonDenda 8 (1489)(11)')
            
            ###999 Denda
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu >0 :
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Materai Denda9')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0 :
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Terposting Dengan baik Materai NonDenda9')
            ###10 Denda
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0 and akad.total_plns_gu < 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_anggota_materai(akad, request.user)
                jurnal_pelunasan_barang_sama_anggota_lebih(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting Dengan Baik Materai  Denda 1544 (2)')
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0 and akad.total_plns_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_anggota(akad,request.user)#### 3 februari 2016
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting Dengan Baik Materai  Denda 1561 (1)')
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0 and akad.total_plns_gu < 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_anggota_lebih_nondenda(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting Dengan Baik Materai NonDenda 1578 (10)')
            elif akad.agnasabah.jenis_keanggotaan == u'1' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0 and akad.total_plns_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_anggota_materai(akad,request.user)
                #jurnal_pelunasan_barang_sama_anggota_non_denda_aja(akad, request.user)
                jurnal_pelunasan_barang_sama_anggota_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting Dengan Baik Materai NonDenda 1595 (9)')

            ####11
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0 and akad.total_plns_gu < 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai  Denda 1614 (4)')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0 and akad.jasa_gu == 0 \
                and akad.total_plns_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_non_denda_terlambat(akad,request.user)### 3 Jan
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai  Denda 1631 (16)')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0 and akad.jasa_gu > 0 \
                and akad.total_plns_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota(akad, request.user)### 3 Jan
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai  Denda 1651 (3)')

            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.total_plns_gu < 0: #### Asli 3 Jan
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai NonDEnda 1596(12)')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.total_plns_gu > 0: ####Tambah kondisi 3 des2016
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                #jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad, request.user)
                jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai NonDEnda 1667(11)')
            ###12Denda
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi == u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(round(akad.jasa))
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik MATERAI 1614')
            ####13
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik MATERAI Denda 1632')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik MATERAI Nondenda 1632')

            ###14 Denda
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai  Denda 1668')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai > akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai NonDenda 1685')
            ###15 Denda
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota(akad, request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai Denda 1703')
             
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai <=  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0:
                akad.status_taksir = 1
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai NonDenda 1720')

            ###16 Denda
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu > 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad, request.user)
                jurnal_pelunasan_barang_sama_non_anggota(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai Denda 1739')
            elif akad.agnasabah.jenis_keanggotaan == u'2' and akad.nilai <= akad.nilai_gu and akad.jenis_transaksi != u'1'\
                and akad.nilai >  akad.taksir.maxpinjaman and akad.bea_materai > 0 and akad.denda_gu == 0:
                akad.status_taksir = 2
                akad.asumsi_jasa = round(akad.asumsi_pendapatan_jasa())
                akad.os_pokok = akad.nilai
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(round(akad.jasa_kendaraan))
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nilai_asuransi = 0
                akad.nilai_provisi = 0
                akad.jns_gu = 1
                akad.save()
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                jurnal_akad_barang_sama_non_anggota_materai(akad,request.user)
                jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad,request.user)
                messages.add_message(request, messages.INFO, 'Jurnal Akad Lebih Terposting dengan Baik Materai NonDenda 1756')
            kasir = KasirGerai(kasir_id = akad.id,nilai = int(akad.nilai_gu) + int(akad.denda_gu) + int(akad.jasa_gu) + \
                int(akad.jurnal_titipan),tanggal = sekarang ,status=2)
            kasir.save()
            barang = Barang.objects.all()
            banding = barang.filter(id = akad.barang_id)
            aa = banding[0]
            bb = int(aa.akad_ulang) + int(1)
            banding.update(akad_ulang = bb,charger = charger,kondisi_charger = kondisi_charger,   
            batre = batre,kondisi_batre = kondisi_batre,keybord = keybord,kondisi_keybord = kondisi_keybord,
            cassing = cassing,kondisi_cassing = kondisi_cassing,layar = layar,kondisi_layar = kondisi_layar,lensa = lensa,
            kondisi_lensa = kondisi_lensa,batre_kamera = batre_kamera,kondisi_batre_kamera = kondisi_batre_kamera,cassing_kamera = cassing_kamera,
            kondisi_cassing_kamera = kondisi_cassing_kamera,optik_ps = optik_ps,kondisi_optik_ps = kondisi_optik_ps,harddisk  = harddisk,
            kondisi_harddisk = kondisi_harddisk,stick  = stick,kondisi_stick = kondisi_stick,
            hdmi  = hdmi,kondisi_hdmi = kondisi_hdmi,remote = remote,kondisi_remote = kondisi_remote,dus = dus,tas = tas,
            accesoris_barang1 = accesoris_barang1,bpkb=bpkb,stnk=stnk,faktur=faktur,gesek_nomesin=gesek_nomesin,gesek_norangka=gesek_norangka,
            password = password,password_barang =password_barang,buka_tutup_gu = 99)
 
            historiakad =  HistoryAkadUlang( nama = akad.agnasabah.nama, norek = akad.norek(), barang = aa,
            id_barang = aa.id, nilai_pinjaman = akad.nilai, jenis_barang = akad.barang_history_akad_ulang(),
            merk = aa.merk, type = aa.type,cu =request.user,mu = request.user)
            historiakad.save()
            messages.add_message(request, messages.INFO, 'Proses akad baru dengan barang sama Berhasil')            
            return HttpResponseRedirect('/')
    else:
        form = BarangBedaForm()
        form.fields['pilih_jasa'].widget = forms.HiddenInput()
    template='gerai/add/input_barang_sama.html'
    variable = RequestContext(request, {'form':form})
    return render_to_response(template,variable)

def jurnal_akad_barang_sama_non_anggota(akad, user):
    D = decimal.Decimal
    sama= AdmGadaiUlangMapper.objects.get(item='6')
    a_non_anggota = sama.coa
    a_titipan_pencairan = sama.coa_1
    a_pendapatan_jasa = sama.coa_2
    a_pendapatan_adm = sama.coa_3
    a_pdp_bea_simpan = sama.coa_4
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pencairan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_non_anggota,
        kredit = 0,debet = D(akad.nilai),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_all())),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pendapatan_adm,
        debet = 0,kredit = D(float(akad.adm_all())),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit = D(float(akad.beasimpan_all())),id_product = '4',status_jurnal ='2',tgl_trans  = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = 0,kredit = round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)



def jurnal_akad_barang_sama_non_anggota_materai(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='8')
    a_non_anggota = sama.coa
    a_titipan_pencairan = sama.coa_1
    a_pendapatan_jasa = sama.coa_2
    a_pendapatan_adm = sama.coa_3
    a_pdp_bea_simpan = sama.coa_4
    a_materai =sama.coa_7
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pencairan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu= user,mu= user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_non_anggota,
        kredit = 0,debet = D(akad.nilai),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_all())),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pendapatan_adm,
        debet = 0,kredit = D(float(akad.adm_all())),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit = D(float(akad.beasimpan_all())),id_product = '4',status_jurnal ='2',tgl_trans  = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_materai,
        debet = 0,kredit = D(akad.bea_materai),
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = 0,kredit = round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) - D(akad.bea_materai)),
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

def jurnal_akad_barang_sama_anggota(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='5')
    a_anggota = sama.coa
    a_titipan_pencairan = sama.coa_1
    a_pendapatan_jasa = sama.coa_2
    a_pendapatan_adm = sama.coa_3
    a_pdp_bea_simpan = sama.coa_4
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pencairan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_anggota,
        kredit = 0,debet = D(akad.nilai),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_all())),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pendapatan_adm,
        debet = 0,kredit = D(float(akad.adm_all())),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit = D(float(akad.beasimpan_all())),id_product = '4',status_jurnal ='2',tgl_trans  = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = 0,kredit = round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,id_cabang =akad.gerai.kode_cabang,id_unit= 300)


def jurnal_akad_barang_sama_anggota_materai(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='7')
    a_anggota = sama.coa
    a_titipan_pencairan = sama.coa_1
    a_pendapatan_jasa = sama.coa_2
    a_pendapatan_adm = sama.coa_3
    a_pdp_bea_simpan = sama.coa_4
    a_materai =sama.coa_7
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pencairan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_anggota,
        kredit = 0,debet = D(akad.nilai),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_all())),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pendapatan_adm,
        debet = 0,kredit = D(float(akad.adm_all())),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit = D(float(akad.beasimpan_all())),id_product = '4',status_jurnal ='2',tgl_trans  = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_materai,
        debet = 0,kredit = D(akad.bea_materai),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = 0,kredit = round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all())-D(akad.bea_materai) ),
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,id_cabang =akad.gerai.kode_cabang,id_unit= 300)



##9 & 11 13 & 14 JURNAL JENIS TRANSAKSI KENDARaAN DAN ELEKTRONIK NILAI > NILAI GU
def jurnal_pelunasan_barang_sama_non_anggota_lebih(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='4')
    a_titipan_pencairan = sama.coa_1
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek_lunas_sblm, akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek_lunas_sblm,cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = D(akad.nilai_gu) + D(float(akad.denda_gu)) + D(float(akad.jasa_gu)),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu) ,debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='12')
    a_titipan_pencairan = sama.coa_1
    a_anggota = sama.coa
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = D(akad.nilai_gu) + D(float(akad.denda_gu)) + D(float(akad.jasa_gu)),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu) ,debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

###8 & 12 & 15 & 16## Jurnal Non ANggota ELEKTRONIK KENDARAAN NILAI > NILAI_GU
def jurnal_pelunasan_barang_sama_non_anggota(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='3')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan = sama.coa_5
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek_lunas_sblm, akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek_lunas_sblm,cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        #debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit =  0, ASLI
        debet =round(D(akad.nilai) - D(akad.jasa_all())- D(akad.beasimpan_all())- D(akad.adm_all())-D(akad.bea_materai) ),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        #debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())\
        #- D(akad.beasimpan_all()) - D(akad.bea_materai)),kredit = 0, ASLI
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu)) + D(akad.adm_all())) - (D(akad.nilai) - D(akad.jasa_all())\
        - D(akad.beasimpan_all()) - D(akad.bea_materai)),
        kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,id_cabang =akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet = 0 ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='11')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan = sama.coa_5
    a_anggota = sama.coa

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        #debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit =  0, ASLI
        debet =round(D(akad.nilai) - D(akad.jasa_all())- D(akad.beasimpan_all())- D(akad.adm_all())-D(akad.bea_materai) ),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        #debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())\
        #- D(akad.beasimpan_all()) - D(akad.bea_materai)),kredit = 0, ASLI
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu)) + D(akad.adm_all())) - (D(akad.nilai) - D(akad.jasa_all())\
        - D(akad.beasimpan_all()) - D(akad.bea_materai)),
        kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet = 0 ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

###1 & 4 & 6 & 7###JURNAL ANGGOTA JENIS ELEKTRONIK NILAI <= NILAI_GU
def jurnal_pelunasan_barang_sama_anggota(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='1')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan =sama.coa_5
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all())-D(akad.bea_materai)),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ) + (D(akad.bea_materai)),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_anggota_nondenda(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='9')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan = sama.coa_5
    a_anggota = sama.coa
    

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        #debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all())),
        debet =(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all())) - \
            (D((akad.denda_gu)) + D((akad.jasa_gu))+D(akad.bea_materai)),
        kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all())) + D(akad.bea_materai),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
###SEPUR TES
def jurnal_pelunasan_barang_sama_anggota_non_denda_aja(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='13')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan =sama.coa_5
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) - D(akad.bea_materai)),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) + D(akad.bea_materai) ),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_anggota_non_denda_terlambat(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='14')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan =sama.coa_5
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)


def jurnal_pelunasan_barang_sama_non_anggota_non_denda_oto(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='15')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan =sama.coa_5
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek_lunas_sblm, akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek_lunas_sblm,cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_non_anggota_non_denda_terlambat(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='16')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan =sama.coa_5
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) - D(akad.bea_materai)),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))+ D(akad.bea_materai)) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)


## AKHIR SEPUR TES
##2 & 3 & 5 & 10### JURNAL ANGGOTA ELEKTRONIK KENDARAAN  NILAI > NILAI_GU
def jurnal_pelunasan_barang_sama_anggota_lebih(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='2')
    a_titipan_pencairan = sama.coa_1
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = D(akad.nilai_gu) + D(float(akad.denda_gu)) + D(float(akad.jasa_gu)),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu) ,debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_anggota_lebih_nondenda(akad, user):
    D = decimal.Decimal
    sama = AdmGadaiUlangMapper.objects.get(item='10')
    a_titipan_pencairan = sama.coa_1
    a_anggota = sama.coa

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = akad.tanggal,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = D(akad.nilai_gu) + D(float(akad.denda_gu)) + D(float(akad.jasa_gu)),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu) ,debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

@login_required
def neracagabungan(request):
    now = datetime.date.today()
    #gr = GeraiGadai.objects.all()
    #ag = gr.akadgadai_set.filter(tanggal=now) 
    #prpj = gr.perpanjang_set.filter(tanggal=now)
    #lunas= gr.pelunasan_set.filter(tanggal=now)    
    #bea = gr.biaya_set.filter(tanggal=now)
    ######gr = GeraiGadai.objects.all()
    ag = AkadGadai.objects.filter(tanggal=now)
    prpj = Perpanjang.objects.filter(tanggal=now)
    lunas= Pelunasan.objects.filter(tanggal=now)
    bea = Biaya.objects.filter(tanggal=now)

    template = 'gerai/rekapneracagabungan.html'
    variable = RequestContext(request, {
        #'gr':gr,
        'ag':ag,
        'prpj':prpj,
        'lunas':lunas,
        'nilai': sum([b.nilai for b in ag ]),
        'jasa': sum([b.tot_jasa_kend_elek for b in ag ]),
        'adm': sum([b.tot_adm_kend_elek for b in ag ]),
        'simpan': sum([b.tot_simpan_kend_elek for b in ag ]),
        'jumlah_biaya' : sum([b.jumlah_biaya for b in ag ]),
        'simpanprpj': sum([b.bea_simpan_total for b in prpj ]),
        'jasaprpj': sum([b.bea_jasa_total for b in prpj ]),
        'dendaprpj': sum([b.denda_total for b in prpj ]), 
        'jumlahbiaya': sum([b.pndptan_prpj_total for b in prpj ]),  
        'terlambat': sum([b.terlambat for b in lunas ]),  
        'denda': sum([b.denda_total for b in lunas ]),  
        'jumlah_lunas': sum ([b.jumlah_pelunasan for b in lunas]), 
        'nilai': sum ([b.nilai for b in lunas]),
        'bea_jasa': sum ([b.bea_jasa_total for b in lunas]),
        'jumlahjasa_lunas': sum ([b.jasa_denda for b in lunas]),
        'tunai_pusat' : sum ([b.tunai for b in bea]),
        'bank' : sum ([b.bank for b in bea]), 
        'dari_gerai':sum([b.dari_gerai for b in bea]),
        'jml_pospay':sum([b.jml_pospay for b in bea]),

        'pln': sum([b.listrik for b in bea]),
        'pdam':sum([b.pdam for b in bea]),
        'tlp':sum([b.telpon for b in bea]),
        'foto_copy':sum([b.foto_copy for b in bea]),
        'majalah':sum([b.majalah for b in bea]),
        'keamanan':sum([b.iuran_keamanan for b in bea]),
        'kebersihan':sum([b.iuran_kebersihan for b in bea]),
        'promosi':sum([b.promosi for b in bea]),
        'air_minum':sum([b.air_minum for b in bea]),
        'sewa':sum([b.sewa_gedung_gerai for b in bea]),
        'setoran_bank':sum([b.setoran_bank for b in bea]),
        'tunai':sum([b.tunai_pickup for b in bea]),
        'kegerai':sum([b.ke_gerai for b in bea]),

        'prangko':sum ([b.prangko for b in bea]), 
        'surat_kilat_khusus': sum ([b.surat_kilat_khusus for b in bea]),
        'paket_pos_standar': sum([b.paket_pos_standar for b in bea]),
        'paket_kilat_khusus': sum([b.paket_kilat_khusus for b in bea]),
        'pos_express':sum([b.pos_express for b in bea]),
        'materai' : sum([b.materai for b in bea]),
        'ems' : sum([b.ems for b in bea]),
        'pendapatan': sum([b.pendapatan_lain for b in bea]), 
        #'total': jumlah_biaya + jumlahjasa_lunas + jumlahbiaya,
    })
    return render_to_response(template,variable)

@login_required
def hapus_permintaan(request,object_id):
    ag = AkadGadai.objects.get(id=object_id)
    ag.tanggal_permintaan =None
    ag.tanggal_pengiriman =None
    ag.klik_permintaan = None
    ag.status_permintaan =None
    ag.save()
    return HttpResponseRedirect("/gerai/%s/show/" % ag.gerai.id)
###Permintaan Gerai###
@login_required
def permintaan(request):
    try :
        f = forms.DateField()
        tanggal_permintaan = f.clean(request.POST.get('tanggal_permintaan',''))
        a = forms.DateTimeField()
        klik_permintaan = a.clean(request.POST.get('klik_permintaan',''))
        form = forms.CharField()
        status_permintaan = form.clean(request.POST.get('status_permintaan',''))
    except :
        return HttpResponseRedirect('/gerai/%s/show/' % (request.POST.get('id', '')))
    for i in request.POST.getlist('id_minta'):
        pk = AkadGadai.objects.get(id=int(i))
        pk.tanggal_permintaan = tanggal_permintaan
        pk.klik_permintaan = klik_permintaan
        pk.status_permintaan = status_permintaan
        pk.tanggal_pengiriman = None
        messages.add_message(request, messages.INFO,' Permintan telah di inputkan.')
        pk.save()

    return HttpResponseRedirect('/gerai/%s/show/' % pk.gerai.kode_cabang)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def cetakminta(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    try :
        f = forms.DateField()
    except :
        try:
            tanggal = AkadGadai.objects.filter(tanggal__month=tanggal_permintaan.month).filter(tanggal_permintaan=True)
        except:
            tanggal = AkadGadai.objects.filter(tanggal__month=tanggal_permintaan.month)
    now = datetime.date.today()
    gr = Tbl_Cabang.objects.get(kode_cabang = cab)
    gerai = gr.akadgadai_set.filter(tanggal_permintaan=now,status_permintaan='1').order_by('gerai')
    rekap_jenis = dict([[k, 0] for k,v in JENIS_BARANG])
    return render(request,'gerai/permintaan.html',{'gr':gr,
        'gerai':gerai,'rekap_jenis': [(dict(JENIS_BARANG)[k], v) for k,v in rekap_jenis.iteritems()]})
###End Permintaan Gerai###

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in= ('ADM_GERAI','KPLGERAI')))
def show(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    aa = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    sekarang1 = datetime.datetime.now()
    aa = Tbl_Cabang.objects.get(kode_cabang=cab)
    gr = aa.akadgadai_set.filter(kepalagerai__status = 1).exclude(sts_tdr = u'1').exclude(status_transaksi__in = ('2','4','5','6','7','8','9','10'))
    variables = RequestContext(request, {'tes':aa,'object':gr,'sekarang':sekarang,'sekarang1':sekarang1})
    return render_to_response('gerai/detail.html', variables)


###cetak Rekap Harian###
@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def cetak_rekap(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    batas = datetime.date(2010,1,1)
    batas_awal = datetime.date(2017,1,1)
    now = datetime.date.today()
    h=now.day
    m=now.month
    y=now.year
    kemarin  = now - relativedelta(days=1)
    aa = now.year
    bb = 1
    cc = 1
    awal = datetime.date(aa,bb,cc)
    gr = Tbl_Cabang.objects.get(kode_cabang = cab)
    ag = gr.akadgadai_set.filter(tanggal=now).filter(jns_gu = 0).filter(kepalagerai__status = 1)
    gu = gr.akadgadai_set.filter(tanggal=now).filter(jns_gu = 1,kepalagerai__status = 1,lunas__isnull = True)
    akad = AkadGadai.objects.filter(tanggal = now,lunas__isnull = True,gerai__kode_cabang=cab,jns_gu = u'0').exclude(status_transaksi__in=('5'))
    akad_pencairan= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__lte=now,gerai__kode_cabang = cab)
    akad_jasa = AkadGadai.objects.filter(tanggal__range=(awal,kemarin),kepalagerai__status = 1,gerai__kode_cabang = cab)
    akad_gu = AkadGadai.objects.filter(tanggal = now).filter(lunas__isnull = True,gerai__kode_cabang=cab,jns_gu = u'2')
    akad_gu_jasaterlambat = AkadGadai.objects.filter(tanggal__range =(awal,now),lunas__isnull=True,gerai__kode_cabang=cab,jns_gu = u'2')
    lunas= gr.pelunasan_set.filter(tanggal=now,sts_plns =1)
    lunas_kemarin= gr.pelunasan_set.filter(tanggal = now).exclude(sts_plns =2)
    lunas_kemarin_jasaterlambat= gr.pelunasan_set.filter(tanggal__range =(awal,kemarin))
    akad_beasimpan = AkadGadai.objects.filter(tanggal__range = (awal,kemarin),gerai__kode_cabang=cab).exclude(status_transaksi = 5)
    akad_adm = AkadGadai.objects.filter(tanggal__range = (awal,kemarin),gerai__kode_cabang=cab).exclude(status_transaksi =5)
    akad_gu_denda = AkadGadai.objects.filter(tanggal__range =(awal,kemarin),gerai__kode_cabang=cab,jns_gu = u'2')
    lunas_kemarin_denda= gr.pelunasan_set.filter(tanggal__range =(awal,kemarin)).exclude(sts_plns =3)
    saldo_akhir_akad = AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).\
        filter(tanggal__lte=now,gerai__kode_cabang = cab)
    saldo_awal_debet = sum([b.nilai for b in ag ]) + sum([b.nilai for b in gu ])
    saldo_awal_kredit = sum([b.nilai for b in lunas ]) + sum([b.nilai_gu for b in gu ])
    saldo_akhir = sum([b.nilai for b in saldo_akhir_akad ])
    saldo_awal = float(sum([b.nilai for b in saldo_akhir_akad ])) + float((sum([b.nilai for b in lunas ]) + sum([b.nilai_gu for b in gu ]) )) - float(sum([b.nilai for b in ag ]) + sum([b.nilai for b in gu ]))

    ##SUM JASA
    saldo_awal_jasa = sum([b.tot_jasa_kend_elek for b in akad_jasa ])#sum([b. for b in akad_jasa ])
    saldo_awal_jasa_kredit= sum([b.jasa_all() for b in ag ])+ sum([b.jasa_all() for b in gu ])
    saldo_akhir_jasa = saldo_awal_jasa + saldo_awal_jasa_kredit
    ##SUM JASA TERLAMBAT
    saldo_awal_jasaterlambat = sum([a.bea_jasa_kendaraan for a in lunas_kemarin_jasaterlambat]) + sum([a.bea_jasa for a in lunas_kemarin_jasaterlambat])
    saldo_awal_jasaterlambat_kredit = sum([b.jasa_gu for b in gu ])+ sum([b.jasa_all() for b in lunas ])
    saldo_akhir_jasaterlambat = saldo_awal_jasaterlambat + saldo_awal_jasaterlambat_kredit

    ##SUM SIMPAN
    saldo_awal_simpan = sum([b.biayasimpan for b in akad_beasimpan ]) + sum([b.beasimpan_kendaraan for b in akad_beasimpan ])
    saldo_awal_simpan_kredit = sum([b.beasimpan_all() for b in ag ])+ sum([b.beasimpan_all() for b in gu ])
    saldo_akhir_simpan = saldo_awal_simpan + saldo_awal_simpan_kredit

    ##SUM ADM
    saldo_awal_adm = sum([b.adm_all() for b in akad_adm ])
    saldo_awal_adm_kredit = sum([b.adm_all() for b in ag ])+ sum([b.adm_all() for b in gu ])
    saldo_akhir_adm = saldo_awal_adm+ saldo_awal_adm_kredit

    ##SUM DENDA
    saldo_awal_denda = sum([b.denda_total for b in lunas_kemarin_denda])
    saldo_awal_denda_kredit = sum([b.denda_gu for b in gu ])+ sum([b.denda_all() for b in lunas ])
    saldo_akhir_denda = saldo_awal_denda + saldo_awal_denda_kredit

    template = 'gerai/pendapatan.html'
    variable = RequestContext(request, {
        'gr':gr,
        'ag':ag,
        'gu':gu,
        'lunas':lunas,
        ## PENCAIRAN
        'total_nilai_pencairan':sum([b.nilai for b in ag ]),
        'total_jasa_pencairan':sum([b.jasa_all() for b in ag ]),
        'total_simpan_pencairan':sum([b.beasimpan_all() for b in ag ]),
        'total_adm_pencairan':sum([b.adm_all() for b in ag ]),
        ##GADAI ULANG AWAL
        'total_nilai_pencairan_gu_awal':sum([b.nilai_gu for b in gu ]),
        'total_jasa_pencairan_gu_awal':sum([b.jasa_gu for b in gu ]),
        'total_denda_pencairan_gu_awal':sum([b.denda_gu for b in gu ]),
        ##GADAI ULANG BARU
        'total_nilai_pencairan_gu':sum([b.nilai for b in gu ]),
        'total_jasa_pencairan_gu':sum([b.jasa_all() for b in gu ]),
        'total_simpan_pencairan_gu':sum([b.beasimpan_all() for b in gu ]),
        'total_adm_pencairan_gu': sum([b.adm_all() for b in gu ]),

        ## PELUNASAN
        ##GADAI ULANG BARU
        'total_nilai_pelunasan':sum([b.nilai for b in lunas ]),
        'total_denda_pelunasan':sum([b.denda_all_rekap() for b in lunas ]),
        'total_jasa_pelunasan':sum([b.jasa_all() for b in lunas ]),
        'total_adm_pencairan_lunas':sum([b.adm_all() for b in ag ]),

        ##SALDO PINJAMAN
        'saldo_awal':saldo_awal,
        'saldo_awal_debet':saldo_awal_debet,
        'saldo_awal_kredit':saldo_awal_kredit,
        'saldo_akhir':saldo_akhir,

        ##SALDO JASA
        'saldo_awal_jasa':saldo_awal_jasa,
        'saldo_awal_jasa_kredit':saldo_awal_jasa_kredit,
        #'saldo_awal_kredit_jasa':saldo_awal_kredit_jasa,
        'saldo_akhir_jasa':saldo_akhir_jasa,

        ##SALDO SIMPAN
        'saldo_awal_simpan':saldo_awal_simpan,
        'saldo_awal_simpan_kredit':saldo_awal_simpan_kredit,
        'saldo_akhir_simpan':saldo_akhir_simpan,

        ##SALDO ADM
        'saldo_awal_adm':saldo_awal_adm,
        'saldo_awal_adm_kredit':saldo_awal_adm_kredit,
        'saldo_akhir_adm':saldo_akhir_adm,

        ##SALDO DENDA
        'saldo_awal_denda':saldo_awal_denda,
        'saldo_awal_denda_kredit':saldo_awal_denda_kredit,
        'saldo_akhir_denda':saldo_akhir_denda,
        #'denda_debet':denda_debet,

        ##SALDO JASA TERLAMBAT
        'saldo_awal_jasaterlambat':saldo_awal_jasaterlambat,
        'saldo_awal_jasaterlambat_kredit':saldo_awal_jasaterlambat_kredit,
        'saldo_akhir_jasaterlambat':saldo_akhir_jasaterlambat,
        #'denda_debet':denda_debet,
    })
    return render_to_response(template,variable)

##cetak Rekap bulanan###
@login_required
def rekap_bulan(request, object_id):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    #tanggal = forms.DateField()
    gr = GeraiGadai.objects.get(id = object_id)
    gerai = gr.akadgadai_set.filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year).order_by('gerai')
        
    template = 'gerai/bulan.html'
    variables = RequestContext(request, {
        'gr':gr,
        'gerai':gerai,
        'tanggal':tanggal,
        'nilai': sum([b.terima_bersih for b in gerai ]),
        'jasa': sum([b.jasa for b in gerai ]),
        'adm': sum([b.adm for b in gerai ]),
        'simpan': sum([b.biayasimpan for b in gerai ]),
    })
    return render_to_response(template,variables)

###cetak Rekap bulanan###
@login_required
def piutang_bulan(request, object_id):
    sekarang = datetime.date.today() 
    gr =GeraiGadai.objects.get(id = object_id)
    gerai = gr.akadgadai_set.order_by('gerai').filter(lunas__isnull = True).filter(lelang__isnull = True)
        
    template = 'gerai/piutang.html'
    variables = RequestContext(request, {
        'gr':gr,
        'gerai':gerai,'tanggal':sekarang,
        'nilai': sum([b.terima_bersih for b in gerai ]),
        'jasa': sum([b.jasa for b in gerai ]),
        'adm': sum([b.adm for b in gerai ]),
        'simpan': sum([b.biayasimpan for b in gerai ]),
        'bersih': sum([b.terima_bersih for b in gerai ]),
        #'simpanprpj': sum([b.bea_simpanprpj for b in gerai]),
    })
    return render_to_response(template,variables)

@login_required
def rekap_piutang(request, object_id):
    sekarang = datetime.date.today() 
    gr =GeraiGadai.objects.get(id = object_id)
    gerai = gr.akadgadai_set.order_by('gerai').filter(lunas__isnull = True).filter(lelang__isnull = True)
        
    template = 'gerai/rekappiutang.html'
    variables = RequestContext(request, {
        'gr':gr,
        'gerai':gerai,'tanggal':sekarang,
        'nilai': sum([b.terima_bersih for b in gerai ]),
        'jasa': sum([b.jasa for b in gerai ]),
        'adm': sum([b.adm for b in gerai ]),
        'simpan': sum([b.biayasimpan for b in gerai ]),
        'bersih': sum([b.terima_bersih for b in gerai ]),
        #'simpanprpj': sum([b.bea_simpanprpj for b in gerai]),
    })
    return render_to_response(template,variables)


###cetak Rekap Unit###
@login_required
def rekapunit(request):
    rekap = GeraiGadai.objects.all()
    kp = []
    for k in rekap:
        if k.akadgadai_set.filter(lunas__isnull= True).count() > 0:
            kp.append(k)
    
    total_aktif = total_pk=total_jasa=total_adm=total_beasimpan=total_materai=total_nilai=total_terimabersih=  0
    
    for k in kp :
        
        total_aktif += k.aktif()
        total_pk += k.aktif()
        total_jasa += k.get_jumlah_jasa()
        total_adm += k.get_jumlah_adm()
        total_beasimpan += k.get_jumlah_beasimpan()
        #total_materai += k.get_jumlah_materai()
        total_nilai += k.get_jumlah_nilai()
        total_terimabersih += k.get_jumlah_terimabersih()

    template = 'gerai/rekap.html'
    variables = RequestContext(request, {
    'kp': kp ,
    'nkp' : len(kp),
    'npk' : total_pk,
    'aktif' : total_aktif,
    'jasa' : total_jasa,
    'adm':total_adm,
    'simpan':total_beasimpan,
    #'materai':total_materai,
    'nilai':total_nilai,
    'terima_bersih':total_terimabersih,
    })
    return render_to_response(template, variables)

@login_required
def neracaunit(request, object_id):
    now = datetime.date.today()
    gr = GeraiGadai.objects.get(id = object_id)
    ag = gr.akadgadai_set.filter(tanggal=now) 
    prpj = gr.perpanjang_set.filter(tanggal=now)
    lunas= gr.pelunasan_set.filter(tanggal=now)    
    bea = gr.biaya_set.filter(tanggal=now)    

    template = 'gerai/rekapneraca.html'
    variable = RequestContext(request, {
        'gr':gr,
        'ag':ag,
        'prpj':prpj,
        'lunas':lunas,
        'nilai': sum([b.nilai for b in ag ]),
        'jasa': sum([b.tot_jasa_kend_elek for b in ag ]),
        'adm': sum([b.tot_adm_kend_elek for b in ag ]),
        'simpan': sum([b.tot_simpan_kend_elek for b in ag ]),
        'jumlah_biaya' : sum([b.jumlah_biaya for b in ag ]),
        'simpanprpj': sum([b.bea_simpan_total for b in prpj ]),
        'jasaprpj': sum([b.bea_jasa_total for b in prpj ]),
        'dendaprpj': sum([b.denda_total for b in prpj ]), 
        'jumlahbiaya': sum([b.pndptan_prpj_total for b in prpj ]),  
        'terlambat': sum([b.terlambat for b in lunas ]),  
        'denda': sum([b.denda_total for b in lunas ]),  
        'jumlah_lunas': sum ([b.jumlah_pelunasan for b in lunas]), 
        'nilai': sum ([b.nilai for b in lunas]),
        'bea_jasa': sum ([b.bea_jasa_total for b in lunas]),
        'jumlahjasa_lunas': sum ([b.jasa_denda for b in lunas]),
        'tunai_pusat' : sum ([b.tunai for b in bea]),
        'bank' : sum ([b.bank for b in bea]), 
        'dari_gerai':sum([b.dari_gerai for b in bea]),
        'jml_pospay':sum([b.jml_pospay for b in bea]),

        'pln': sum([b.listrik for b in bea]),
        'pdam':sum([b.pdam for b in bea]),
        'tlp':sum([b.telpon for b in bea]),
        'foto_copy':sum([b.foto_copy for b in bea]),
        'majalah':sum([b.majalah for b in bea]),
        'keamanan':sum([b.iuran_keamanan for b in bea]),
        'kebersihan':sum([b.iuran_kebersihan for b in bea]),
        'promosi':sum([b.promosi for b in bea]),
        'air_minum':sum([b.air_minum for b in bea]),
        'sewa':sum([b.sewa_gedung_gerai for b in bea]),
        'setoran_bank':sum([b.setoran_bank for b in bea]),
        'tunai':sum([b.tunai_pickup for b in bea]),
        'kegerai':sum([b.ke_gerai for b in bea]),

        'prangko':sum ([b.prangko for b in bea]), 
        'surat_kilat_khusus': sum ([b.surat_kilat_khusus for b in bea]),
        'paket_pos_standar': sum([b.paket_pos_standar for b in bea]),
        'paket_kilat_khusus': sum([b.paket_kilat_khusus for b in bea]),
        'pos_express':sum([b.pos_express for b in bea]),
        'materai' : sum([b.materai for b in bea]),
        'ems' : sum([b.ems for b in bea]),
        'pendapatan': sum([b.pendapatan_lain for b in bea]), 
        #'total': jumlah_biaya + jumlahjasa_lunas + jumlahbiaya,
    })
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def sjalan(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0]
    now = datetime.date.today()
    gr = Tbl_Cabang.objects.get(kode_cabang = cab)
    gerai = gr.akadgadai_set.filter(tanggal=now).exclude(lunas=now).filter(tanggal__year=tanggal.year).order_by('gerai')
    brg_retur = gr.akadgadai_set.filter(tanggal_permintaan=now,status_permintaan="2").order_by('gerai')
    rekap_jenis = dict([[k, 0] for k,v in JENIS_BARANG])
    return render(request,'gerai/suratjalan.html',{'gr':gr,'gerai':gerai,'tanggal':tanggal,
        'rekap_jenis': [(dict(JENIS_BARANG)[k], v) for k,v in rekap_jenis.iteritems()],'brg_retur':brg_retur})

###Rekap Transaksi Harian All Gerai###  
@login_required
def rekap_allgerai_harian(request):
    now = datetime.date.today()
    rekap = GeraiGadai.objects.all()
    pk = []
    for k in rekap:
        if k.akadgadai_set.filter(tanggal=now).filter(lunas__isnull= True).count() > 0:
            pk.append(k)
    
    total_aktif = total_pk=total_jasa=total_adm=total_beasimpan=total_nilai=total_pendapatan=  0
    
    for k in pk :
        
        total_aktif += k.aktif_harian()
        total_pk += k.aktif_harian()
        total_jasa += k.get_jumlah_jasa_harian()
        total_adm += k.get_jumlah_adm_harian()
        total_beasimpan += k.get_jumlah_beasimpan_harian()
        total_nilai += k.get_jumlah_nilai_harian()
        total_pendapatan += k.total_pendapatan_harian()
        
    template = 'gerai/rekap_allgerai_harian.html'
    variables = RequestContext(request, {
    'pk': pk ,
    'nkp' : len(pk),
    'npk' : total_pk,
    'aktif' : total_aktif,
    'jasa' : total_jasa,
    'adm':total_adm,
    'simpan':total_beasimpan,
    'nilai':total_nilai,
    'total_pendapatan_harian':total_pendapatan,
    })
    return render_to_response(template, variables)

@login_required
def prpj_allgerai_harian(request):
    now = datetime.date.today()
    rekap = GeraiGadai.objects.all()
    ppj = []
    for k in rekap:
        if k.perpanjang_set.filter(tanggal=now).count() > 0:
            ppj.append(k)
    
    total_aktif_ppj = total_ppj=total_jasa_ppj=total_beasimpan_ppj=total_denda_ppj=total_nilai_ppj=total_pendapatan_ppj=  0
    
    for k in ppj :
        
        total_aktif_ppj += k.aktif_prpj_harian()
        total_ppj += k.aktif_prpj_harian()
        #total_jasa_ppj += k.prpj_jasa_harian()
        total_beasimpan_ppj += k.prpj_beasimpan_harian()
        total_denda_ppj += k.prpj_denda_harian()
        total_nilai_ppj += k.prpj_nilai_harian()
        total_pendapatan_ppj += k.total_prpj_pendapatan_harian()
        
    template = 'gerai/prpj_allgerai_harian.html'
    variables = RequestContext(request, {
    'ppj': ppj ,
    'nkp' : len(ppj),
    'npk' : total_ppj,
    'aktif' : total_aktif_ppj,
    #'jasa' : total_jasa_ppj,
    'simpan':total_beasimpan_ppj,
    'denda':total_denda_ppj,
    'nilai':total_nilai_ppj,
    'total_pendapatan_ppj':total_pendapatan_ppj,
    })
    return render_to_response(template, variables)

@login_required
def pelunasan_allgerai_harian(request):
    now = datetime.date.today()
    rekap = GeraiGadai.objects.all()
    plns = []
    for k in rekap:
        if k.pelunasan_set.filter(tanggal=now).count() > 0:
            plns.append(k)
    
    total_aktif_plns = total_plns=total_jasa_plns=total_denda_plns=total_nilai_plns=total_pendapatan_plns=  0
    
    for k in plns :
        
        total_aktif_plns += k.aktif_plns_harian()
        total_plns += k.aktif_plns_harian()
        total_jasa_plns += k.plns_jasa_harian()
        total_denda_plns += k.plns_denda_harian()
        total_nilai_plns += k.plns_nilai_harian()
        total_pendapatan_plns += k.total_pelunasan_jasa_harian()
        
    template = 'gerai/pelunasan_allgerai_harian.html'
    variables = RequestContext(request, {
    'plns': plns ,
    'nkp' : len(plns),
    'npk' : total_plns,
    'aktif' : total_aktif_plns,
    'jasa' : total_jasa_plns,
    'denda':total_denda_plns,
    'nilai':total_nilai_plns,
    'total_pendapatan_plns':total_pendapatan_plns,
    })
    return render_to_response(template, variables)
 ###End Rekap Transaksi Harian All Gerai###     

####modifikasi####
@login_required
def list(request):    
    tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    return HttpResponseRedirect("/gerai/arsip/?tgl=%s" % tanggal.strftime('%Y-%m-%d') )

@login_required
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
           
        
        
    template = 'gerai/list_day.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__year=tanggal.year).filter(tanggal__month=tanggal.month),
        'month_list': AkadGadai.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : AkadGadai.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

@login_required
def gerai_bulan(request):
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
        
        bn = AkadGadai.objects.filter(gerai = b ).filter(tanggal__month=tanggal.month).filter(tanggal__year=tanggal.year).order_by('no').order_by('cu')
    
        for akadgadai in bn :
            gerai.append(akadgadai)    
           
        
        
    template = 'gerai/list_month.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': AkadGadai.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : AkadGadai.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

@login_required
def rekaphari(request, object_id):
    tanggal = forms.DateField().clean(request.GET.get('tgl',''))
            
    barang = AkadGadai.objects.filter(gerai= str(object_id)).filter(tanggal = tanggal).order_by('gerai')
    
    template = 'gerai/rekaphari.html'
    variables = RequestContext(request, {
        'barang': barang,
        'tanggal' : tanggal,
        'nilai': sum([b.nilai for b in barang ]),
        'jasa': sum([b.jasa for b in barang ]),
        'adm': sum([b.adm for b in barang ]),
        'simpan': sum([b.biayasimpan for b in barang ]),
        'bersih' : sum([b.jumlah_biaya for b in barang ]),
    })    
    return render_to_response(template, variables)

@login_required
def rekapbulan(request, object_id):    
    tanggal = forms.DateField().clean(request.GET.get('tgl',''))
            
    barang = AkadGadai.objects.filter(gerai= str(object_id)).filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year).order_by('gerai')
    template = 'gerai/rekapbulan.html'
    variables = RequestContext(request, {
        'barang': barang,
        'tanggal' : tanggal,
        'nilai': sum([b.nilai for b in barang ]),
        'jasa': sum([b.jasa for b in barang ]),
        'adm': sum([b.adm for b in barang ]),
        'simpan': sum([b.biayasimpan for b in barang ]),
        'bersih' : sum([b.terima_bersih for b in barang ]),
    })    
    return render_to_response(template, variables)

@login_required
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
        
    
    template = 'gerai/list_year.html'

    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': AkadGadai.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : AkadGadai.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai ,
        })    
    return render_to_response(template, variables)

#total transaksi harian,pelunasan,perpanjangan,pencairan
@login_required
def total_harian(request):
    now = datetime.date.today()
    rekap = GeraiGadai.objects.all()
    plns = []
    for k in rekap:
        if k.akadgadai_set.filter(tanggal=now).count()>=0:
            plns.append(k)
    
    total_harian_jasa = total_harian_denda=total_harian_beasimpan=akumulasi_pendapatan_harian=aktif_nasabah_harian=total_harian_adm=nilai_pencairan_harian=prpj_nilai_harian=plns_nilai_harian=total_prpj_beaterlambat_all= 0
    for k in plns :
        
        aktif_nasabah_harian += k.aktif_nasabah_harian()
        total_harian_jasa += k.total_harian_jasa()
        total_harian_denda += k.total_harian_denda()
        total_harian_beasimpan += k.total_harian_beasimpan()
        total_harian_adm +=k.adm_harian()
        akumulasi_pendapatan_harian += k.akumulasi_pendapatan_harian()
        prpj_nilai_harian += k.prpj_nilai_harian()
        plns_nilai_harian += k.plns_nilai_harian()
        nilai_pencairan_harian += k.nilai_pencairan_harian()
        total_prpj_beaterlambat_all += k.total_prpj_beaterlambat_all()
                
    template = 'gerai/total_harian.html'
    variables = RequestContext(request, {
    'plns': plns ,
    'total' : aktif_nasabah_harian,
    'adm' : total_harian_adm,
    'aktif_nasabah_harian' : aktif_nasabah_harian,####tedi
    'jasa' : total_harian_jasa,
    'denda':total_harian_denda,
    'beasimpan':total_harian_beasimpan,
    'akumulasi_pendapatan_harian':akumulasi_pendapatan_harian,
    'akumulasi_pencairan_harian':nilai_pencairan_harian,
    'akumulasi_perpanjangan_harian':prpj_nilai_harian,
    'akumulasi_pelunasan_harian':plns_nilai_harian,
    'total_terlambat':total_prpj_beaterlambat_all,
    })
    return render_to_response(template, variables)

@login_required
def simulasi(request):
    tb = terbilang
    template = 'gerai/simulasi.html'
    variables = RequestContext(request, {'tb':tb})
    return render_to_response(template,variables)


####END REQUEST MANOP GADAI REKAP PENCAIRAN PRPJ PLNS ALL GERAI (PAK DEDI) (02 APRIL 2013)####
###Rekap Pencairan Bulanan  All Gerai###  
@login_required
def pencairan_bulanan_allgerai(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 

    
    rekap = GeraiGadai.objects.all()
    pk = []
    for k in rekap:
        if k.akadgadai_set.filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year).count() > 0:
            pk.append(k)
    
    total_aktif = total_pk=total_jasa=total_adm=total_beasimpan=total_nilai=total_pendapatan=  0
    
    for k in pk :
        
        total_aktif += k.all_aktif_bulanan()
        total_pk += k.all_aktif_bulanan()
        total_jasa += k.get_jumlah_jasa_bulanan()
        total_adm += k.get_jumlah_adm_bulanan()
        total_beasimpan += k.get_jumlah_beasimpan_bulanan()
        total_nilai += k.get_jumlah_nilai_bulanan()
        total_pendapatan += k.total_pendapatan_bulanan()
        
    template = 'gerai/pencairan_bulanan_allgerai.html'
    variables = RequestContext(request, {
    'pk': pk ,
    'nkp' : len(pk),
    'npk' : total_pk,
    'aktif' : total_aktif,
    'jasa' : total_jasa,
    'adm':total_adm,
    'simpan':total_beasimpan,
    'nilai':total_nilai,
    'total_pendapatan_bulanan':total_pendapatan,
    })                                                                                                                                                                                                                  
    return render_to_response(template, variables)
###End Rekap Pencairan Bulanan  All Gerai###  
    
    
###Rekap Perpanjangan Bulanan  All Gerai###  
@login_required
def prpj_bulanan_allgerai(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  Perpanjang.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Perpanjang.objects.dates('tanggal', 'day', order="DESC")[0] 

    
    rekap = GeraiGadai.objects.all()
    pk = []
    for k in rekap:
        if k.perpanjang_set.filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year).count() > 0:
            pk.append(k)
    
    total_aktif = total_pk=total_jasa=total_jasaterlambat=total_denda=total_beasimpan=total_nilai=total_pendapatan=  0
    
    for k in pk :
        
        total_aktif += k.aktif_prpj_bulanan()
        total_pk += k.aktif_prpj_bulanan()
        total_jasa += k.prpj_jasa_bulanan()
        total_jasaterlambat += k.prpj_jasaterlambat_bulanan()
        total_denda += k.prpj_denda_bulanan()
        total_beasimpan += k.prpj_beasimpan_bulanan()
        total_nilai += k.prpj_nilai_bulanan()
        total_pendapatan += k.total_prpj_pendapatan_bulanan()
        
    template = 'gerai/prpj_bulanan_allgerai.html'
    variables = RequestContext(request, {
    'pk': pk ,
    'nkp' : len(pk),
    'npk' : total_pk,
    'aktif' : total_aktif,
    'jasa' : total_jasa,
    'jasaterlambat' : total_jasaterlambat,
    'denda':total_denda,
    'simpan':total_beasimpan,
    'nilai':total_nilai,
    'total_pendapatan_bulanan':total_pendapatan,
    })                                                                                                                                                                                                                  
    return render_to_response(template, variables)
###End Rekap Perpanjangan Bulanan  All Gerai###   
 
###Rekap Perpanjangan Bulanan  All Gerai###  
@login_required
def plns_bulanan_allgerai(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  Pelunasan.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Pelunasan.objects.dates('tanggal', 'day', order="DESC")[0] 

    
    rekap = GeraiGadai.objects.all()
    pk = []
    for k in rekap:
        if k.pelunasan_set.filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year).count() > 0:
            pk.append(k)
    
    total_aktif = total_pk=total_jasa=total_denda=total_nilai=total_pendapatan=  0
    
    for k in pk :
        
        total_aktif += k.aktif_plns_bulanan()
        total_pk += k.aktif_plns_bulanan()
        total_jasa += k.plns_jasa_bulanan()
        total_denda += k.plns_denda_bulanan()
        total_nilai += k.plns_nilai_bulanan()
        total_pendapatan += k.total_plns_pendapatan_bulanan()
        
    template = 'gerai/plns_bulanan_allgerai.html'
    variables = RequestContext(request, {
    'pk': pk ,
    'nkp' : len(pk),
    'npk' : total_pk,
    'aktif' : total_aktif,
    'jasa' : total_jasa,
    'denda':total_denda,
    'nilai':total_nilai,
    'total_pendapatan_bulanan':total_pendapatan,
    })                                                                                                                                                                                                                  
    return render_to_response(template, variables)
###End Rekap Perpanjangan Bulanan  All Gerai###  
####END REQUEST MANOP GADAI REKAP PENCAIRAN PRPJ PLNS ALL GERAI (PAK DEDI) (02 APRIL 2013)####
###firman 15 april 2013
@login_required
def rekap_biaya_harian(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl'))
    except :
        try:
            tanggal =  Biaya.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Biaya.objects.dates('tanggal', 'day', order="DESC")[0] 
    now = datetime.date.today()
    gr = GeraiGadai.objects.all()
    kp = []
    for k in gr:
        if k.biaya_set.filter(tanggal=now):
            kp.append(k)
    totalbiaya_harian = totalpospay = saldo_awal_gerai = totalkas_setoran =total_harian_jasa = total_harian_denda=total_harian_beasimpan=total_harian_adm = akumulasi_pendapatan_harian =0   
    for k in kp:
        totalbiaya_harian = k.totalbiaya_harian() 
        totalpospay = k.totalpospay()
        totalkas_setoran =k.totalkas_setoran()
        total_harian_jasa += k.total_harian_jasa()
        total_harian_denda += k.total_harian_denda()
        total_harian_beasimpan += k.total_harian_beasimpan()
        total_harian_adm +=k.adm_harian()
        akumulasi_pendapatan_harian += k.akumulasi_pendapatan_harian()
    template = 'biaya/list_biaya_gerai.html'
    variable = RequestContext(request, {
        'kp':kp,
        'list_hari' : Biaya.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': Biaya.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : Biaya.objects.dates('tanggal', 'year', order="DESC"),
        #'tunai_pusat' : sum ([b.tunai for b in k]),
         
    })
    return render_to_response(template,variable)

@login_required
def rekap_pendapatan_gerai(request):
    now = datetime.date.today()
    gr = GeraiGadai.objects.all()
    kp = []
    for k in gr:
        if k.biaya_set.filter(tanggal=now):
            kp.append(k)
    totalbiaya_harian = totalpospay = saldo_awal_gerai = totalkas_setoran =total_harian_jasa = total_harian_denda=total_harian_beasimpan=total_harian_adm = akumulasi_pendapatan_harian =0   
    for k in kp:
        totalbiaya_harian = k.totalbiaya_harian() 
        totalpospay = k.totalpospay()
        totalkas_setoran =k.totalkas_setoran()
        total_harian_jasa += k.total_harian_jasa()
        total_harian_denda += k.total_harian_denda()
        total_harian_beasimpan += k.total_harian_beasimpan()
        total_harian_adm +=k.adm_harian()
        akumulasi_pendapatan_harian += k.akumulasi_pendapatan_harian()
    template = 'biaya/list_pendapatan_gerai.html'
    variable = RequestContext(request, {
        'kp':kp,
        #'tunai_pusat' : sum ([b.tunai for b in k]),
         
    })
    return render_to_response(template,variable)

@login_required
def rekap_pengeluaran_gerai(request):
    now = datetime.date.today()
    gr = GeraiGadai.objects.all()
    kp = []
    for k in gr:
        if k.biaya_set.filter(tanggal=now):
            kp.append(k)
    totalbiaya_harian = totalpospay = saldo_awal_gerai = totalkas_setoran =total_harian_jasa = total_harian_denda=total_harian_beasimpan=total_harian_adm = akumulasi_pendapatan_harian =0   
    for k in kp:
        totalbiaya_harian = k.totalbiaya_harian() 
        totalpospay = k.totalpospay()
        totalkas_setoran =k.totalkas_setoran()
        total_harian_jasa += k.total_harian_jasa()
        total_harian_denda += k.total_harian_denda()
        total_harian_beasimpan += k.total_harian_beasimpan()
        total_harian_adm +=k.adm_harian()
        akumulasi_pendapatan_harian += k.akumulasi_pendapatan_harian()
    template = 'biaya/list_pengeluaran_gerai.html'
    variable = RequestContext(request, {
        'kp':kp,
        #'tunai_pusat' : sum ([b.tunai for b in k]),
         
    })
    return render_to_response(template,variable)

@login_required
def list_hari(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl'))
    except :
        try:
            tanggal =  Biaya.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Biaya.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    now = datetime.date.today()
    gr = GeraiGadai.objects.all()
    kp = []
    for k in gr:
        if k.biaya_set.filter(tanggal=tanggal):
            kp.append(k)
    totalbiaya_harian = totalpospay = saldo_awal_gerai = totalkas_setoran =total_harian_jasa = total_harian_denda=total_harian_beasimpan=total_harian_adm = akumulasi_pendapatan_harian =0   
    for k in kp:
        totalbiaya_harian = k.totalbiaya_harian() 
        totalpospay = k.totalpospay()
        totalkas_setoran =k.totalkas_setoran()
        total_harian_jasa += k.total_harian_jasa()
        total_harian_denda += k.total_harian_denda()
        total_harian_beasimpan += k.total_harian_beasimpan()
        total_harian_adm +=k.adm_harian()
        akumulasi_pendapatan_harian += k.akumulasi_pendapatan_harian()
  
    template = 'biaya/list_biaya_gerai.html'
    variable = RequestContext(request, {
        'kp':kp,
        'tanggal' : tanggal,
        'list_hari' : Biaya.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'list_bulan': Biaya.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'list_tahun' : Biaya.objects.dates('tanggal', 'year', order="DESC"),
        #'tunai_pusat' : sum ([b.tunai for b in k]),
         
    })
    return render_to_response(template,variable)

@login_required
def list_bulan(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl'))
    except :
        try:
            tanggal =  Biaya.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Biaya.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    now = datetime.date.today()
    gr = GeraiGadai.objects.all()
    kp = []
    for k in gr:
        if k.biaya_set.filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year).count() > 0:
            kp.append(k)
    totalbiaya_harian = totalpospay = saldo_awal_gerai = totalkas_setoran =total_harian_jasa = total_harian_denda=total_harian_beasimpan=total_harian_adm = akumulasi_pendapatan_harian =0   
    for k in kp:
        totalbiaya_harian = k.totalbiaya_harian() 
        totalpospay = k.totalpospay()
        totalkas_setoran =k.totalkas_setoran()
        total_harian_jasa += k.total_harian_jasa()
        total_harian_denda += k.total_harian_denda()
        total_harian_beasimpan += k.total_harian_beasimpan()
        total_harian_adm +=k.adm_harian()
        akumulasi_pendapatan_harian += k.akumulasi_pendapatan_harian()
    template = 'biaya/list_biaya_gerai.html'
    variable = RequestContext(request, {
        'kp':kp,
        'tanggal' : tanggal,
        'day_list' : Biaya.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': Biaya.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : Biaya.objects.dates('tanggal', 'year', order="DESC"),
        #'tunai_pusat' : sum ([b.tunai for b in k]),
         
    })
    return render_to_response(template,variable)

@login_required    
def list_tahun(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl'))
    except :
        try:
            tanggal =  Biaya.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Biaya.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    now = datetime.date.today()
    gr = GeraiGadai.objects.all()
    kp = []
    for k in gr:
        if k.biaya_set.filter(tanggal__year=tanggal.year).count() > 0:
            kp.append(k)
    totalbiaya_harian = totalpospay = saldo_awal_gerai = totalkas_setoran =total_harian_jasa = total_harian_denda=total_harian_beasimpan=total_harian_adm = akumulasi_pendapatan_harian =0   
    for k in kp:
        totalbiaya_harian = k.totalbiaya_harian() 
        totalpospay = k.totalpospay()
        totalkas_setoran =k.totalkas_setoran()
        total_harian_jasa += k.total_harian_jasa()
        total_harian_denda += k.total_harian_denda()
        total_harian_beasimpan += k.total_harian_beasimpan()
        total_harian_adm +=k.adm_harian()
        akumulasi_pendapatan_harian += k.akumulasi_pendapatan_harian()
    template = 'biaya/list_biaya_gerai.html'
    variable = RequestContext(request, {
        'kp':kp,
        'tanggal' : tanggal,
        'day_list' : Biaya.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': Biaya.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : Biaya.objects.dates('tanggal', 'year', order="DESC"),
        #'tunai_pusat' : sum ([b.tunai for b in k]),
         
    })
    return render_to_response(template,variable)
