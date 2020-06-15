from django.shortcuts import render_to_response, get_object_or_404,render
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
import xlwt
import io
import xlsxwriter
from datetime import datetime
from gadai.xlsxwriter.workbook import Workbook
import datetime
from gadai.appgadai.kplgerai.forms import *
from gadai.appgadai.akadgadai.forms import *
from gadai.appgadai.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.simple import direct_to_template

def price_list(request):
    sekarang = datetime.date.today()
    D = decimal.Decimal
    form = PriceListForm()
    template = 'kplgerai/price_list.html'
    variable = RequestContext(request, {'form':form})
    return render_to_response(template,variable)


def app_edit(request,object_id):
    sekarang = datetime.date.today()
    D = decimal.Decimal
    nas = AkadGadai.objects.get(id=object_id)
   
    form = Edit_AkadForm(initial={'agnasabah':nas.agnasabah.id,'barang':nas.barang.id,'nilai':int(nas.nilai),'gerai':nas.gerai.id,'tanggal':nas.tanggal,
         'jangka_waktu':nas.jangka_waktu,'jangka_waktu_kendaraan':nas.jangka_waktu_kendaraan,'taksir':nas.taksir,
         'jenis_transaksi':nas.jenis_transaksi,'jatuhtempo':nas.jatuhtempo,'nilai_jasa':nas.nilai_jasa,
         'nilai_jasa_kendaraan':nas.nilai_jasa_kendaraan,'nilai_biayasimpan':nas.nilai_biayasimpan,
         'nilai_beasimpan_kendaraan':nas.nilai_beasimpan_kendaraan,'nilai_adm':nas.nilai_adm,'asumsi_jasa':nas.asumsi_jasa,
         'nilai_adm_kendaraan':nas.nilai_adm_kendaraan})
    form.fields['barang'].widget = forms.HiddenInput()
    template = 'akadgadai/edit_akad.html'
    variable = RequestContext(request, {'form':form,'nas':nas})
    return render_to_response(template,variable)

def edit_akad(request, object_id): 
    ag = get_object_or_404(AkadGadai, id=object_id)
    form = Edit_AkadForm(request.POST or None, instance=ag)
    if form.is_valid():
        form.save()
        if ag.agnasabah.jenis_keanggotaan == u'1':
            messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil')
            jurnal_pencairan_edit(ag, request.user)
        elif ag.agnasabah.jenis_keanggotaan == u'2':
            messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil')
            jurnal_pencairan_nonanggota_edit(ag, request.user)
        messages.add_message(request, messages.INFO, 'Akadgadai no rek : %s Berhasil Diedit" % ag.norek()')
        return HttpResponseRedirect(ag.get_absolute_url())
    return direct_to_template(request, 'akadgadai/edit_akad.html', {'form': form}) 

def jurnal_pencairan_edit(ag, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_pinjaman = get_object_or_404(Tbl_Akun, id=163L)
    a_pdp_adm = get_object_or_404(Tbl_Akun, id='430')
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='383')
    a_pdp_bea_simpan = get_object_or_404(Tbl_Akun, id='429')
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),tgl_trans =ag.tanggal,nobukti=ag.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = ag.nilai,kredit = 0,
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
    
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_adm,
        debet = 0,kredit = D(float(ag.adm_all())),
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,debet = 0,kredit =  D(float(ag.jasa_all())),
        id_product = '4',status_jurnal ='2',id_cabang = ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit =  D(float(ag.beasimpan_all())),
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        debet = 0 ,  kredit = round(D(ag.nilai) - D(ag.adm_all()) - ag.jasa_all() - ag.beasimpan_all()),
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)


def jurnal_pencairan_nonanggota_edit(ag, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_pinjaman = get_object_or_404(Tbl_Akun, id=166L)
    a_pdp_adm = get_object_or_404(Tbl_Akun, id='432')
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='383')
    a_pdp_bea_simpan = get_object_or_404(Tbl_Akun, id='429')
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),tgl_trans =ag.tanggal,nobukti=ag.norek(),
        kode_cabang = ag.gerai.kode_cabang,object_id=ag.norek_id(),cu = user,mu=user)
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = ag.nilai,kredit = 0,
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_adm,
        debet = 0,kredit = D(float(ag.adm_all())),
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,
        debet = 0,kredit =  D(float(ag.jasa_all())),
        id_product = '4',status_jurnal ='2',
        id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit =  D(float(ag.beasimpan_all())),
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        debet = 0 , kredit = round(D(ag.nilai) - D(ag.adm_all()) - ag.jasa_all() - ag.beasimpan_all()),#D(ag.jasa_all()) 
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)




def reset_status_tolak(request,object_id):
    kp = KepalaGerai.objects.get(id=object_id)
    kp.delete()
    return HttpResponseRedirect("/") 

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def data_approve_kplg(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    gr = Tbl_Cabang.objects.get(kode_cabang =cab)
    kpl = KepalaGerai.objects.filter(kepala_gerai__gerai=gr)
    akad = AkadGadai.objects.filter(gerai=gr)
    return render(request,'kplgerai/approve_approve_kplg.html',{'kpl': kpl,'gerai':gr,'akad':akad})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KPLGERAI'))    
def approve_pencairan(request,object_id):
    kpl = AkadGadai.objects.get(id=object_id)
    sekarang= datetime.date.today()
    form = KepalaGeraiForm(initial={'kepala_gerai': kpl.id,'tanggal': sekarang})
    form.fields['kepala_gerai'].widget = forms.HiddenInput()
    template = 'kplgerai/approve_pencairan.html'
    variable = RequestContext(request, {'kpl': kpl,'form':form})
    return render_to_response(template,variable)

#@login_required
#@user_passes_test(lambda u: u.groups.filter(name='KPLGERAI'))
def verifikasi_kg_pencairan(request, object_id):
    kpl = AkadGadai.objects.get(id=object_id)
    if request.method == 'POST':
        form = KepalaGeraiForm(request.POST)
        if form.is_valid():
            kepala_gerai = form.cleaned_data['kepala_gerai']   
            tanggal = form.cleaned_data['tanggal']
            status = form.cleaned_data['status']
            note = form.cleaned_data['note']
            kp_gerai = KepalaGerai(kepala_gerai=kepala_gerai,tanggal=tanggal,status=status,note=note)
            kp_gerai.save()
            materai = Biaya_Materai_Cab(gerai_id = kpl.gerai.id,tanggal=tanggal,nilai=kpl.bea_materai,keterangan='Materai Pencairan',\
               norek= kpl.norek())
            materai.save()
            if kp_gerai.status == '2':
                kpl.status_transaksi = '5'
                kpl.save()
                messages.add_message(request, messages.INFO, 'DATA DITOLAK')
            if kp_gerai.status == '1':
                ####ELEKTRONIK ANGGOTA
                if  kpl.jenis_transaksi == u'1' and kpl.nilai > kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1' \
                    and kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil Anggota 1 Materai')
                    kpl.save()
                    jurnal_pencairan(kpl, request.user)
                elif  kpl.jenis_transaksi == u'1' and kpl.nilai > kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1'\
                    and kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil Anggota 2 Non Materai')
                    kpl.save()
                    jurnal_pencairan_nonmaterai(kpl, request.user)                    
                
                elif kpl.jenis_transaksi == u'1' and kpl.nilai <=  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1' \
                    and kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil Anggota Materai 3')
                    kpl.save()
                    jurnal_pencairan(kpl, request.user)

                elif kpl.jenis_transaksi == u'1' and kpl.nilai <=  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1' \
                    and kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Anggota) (Non Materai) 4')
                    kpl.save()
                    jurnal_pencairan_nonmaterai(kpl, request.user)                    
                ####ELEKTRONIK ANGGOTA 
                ####ELEKTRONIK NON ANGGOTA
                elif kpl.jenis_transaksi == u'1' and kpl.nilai >  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2' \
                    and kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Materai) 5')
                    kpl.save()
                    jurnal_pencairan_nonanggota(kpl, request.user)

                elif kpl.jenis_transaksi == u'1' and kpl.nilai >  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2' \
                    and kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Materai) 6')
                    kpl.save()
                    jurnal_pencairan_nonanggota_nonmaterai(kpl, request.user)

                elif kpl.jenis_transaksi == u'1' and kpl.nilai <=  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2' \
                    and kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Materai) 7')
                    kpl.save()
                    jurnal_pencairan_nonanggota(kpl, request.user)                
               
                elif kpl.jenis_transaksi == u'1' and kpl.nilai <=  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2' \
                    and kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Non Materai) 8')
                    kpl.save()
                    jurnal_pencairan_nonanggota_nonmaterai(kpl, request.user)
                ####ELEKTRONIK NON ANGGOTA AKHIR
                ###KENDARAAN NEW MOTOR Anggota
                elif kpl.jenis_transaksi == u'2' and kpl.nilai > kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1' and \
                    kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    kpl.nilai_asuransi = 0
                    kpl.nilai_provisi = 0
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil 9 Materai')
                    kpl.save()
                    jurnal_pencairan(kpl, request.user)

                elif kpl.jenis_transaksi == u'2' and kpl.nilai > kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1' \
                    and kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    kpl.nilai_asuransi = 0
                    kpl.nilai_provisi = 0
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil 10 Non Materai')
                    kpl.save()
                    jurnal_pencairan_nonmaterai(kpl, request.user)
    
                elif kpl.jenis_transaksi == u'2' and kpl.nilai <= kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1'\
                    and kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil 11')
                    kpl.save()
                    jurnal_pencairan(kpl, request.user)

                elif kpl.jenis_transaksi == u'2' and kpl.nilai <= kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1'\
                    and kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil 12')
                    kpl.save()
                    jurnal_pencairan_nonmaterai(kpl, request.user)
                ####MOTOR ANGGOTA
                ####MOTOR NON ANGGOTA
                elif kpl.jenis_transaksi == u'2' and kpl.nilai > kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2'\
                    and kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil 13')
                    kpl.save()
                    jurnal_pencairan_nonanggota(kpl, request.user)
                 
                elif kpl.jenis_transaksi == u'2' and kpl.nilai > kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2'\
                    and kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil 14')
                    kpl.save()
                    jurnal_pencairan_nonanggota_nonmaterai(kpl, request.user)
                
                elif kpl.jenis_transaksi == u'2' and kpl.nilai <= kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2'\
                    and kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil 15')
                    kpl.save()
                    jurnal_pencairan_nonanggota(kpl, request.user)

                elif kpl.jenis_transaksi == u'2' and kpl.nilai <= kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2'\
                    and kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil 16')
                    kpl.save()
                    jurnal_pencairan_nonanggota_nonmaterai(kpl, request.user)
                ###KENDARAAN NEW MOTOR AKHIR
                ###MOBIL ANGGOTA
                elif kpl.jenis_transaksi == u'3' and kpl.nilai > kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1' and \
                    kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Non Materai) 17')
                    kpl.save()
                    jurnal_pencairan(kpl, request.user)
                elif kpl.jenis_transaksi == u'3' and kpl.nilai >  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1' and \
                    kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Non Materai) 18')
                    kpl.save()
                    jurnal_pencairan_nonmaterai(kpl, request.user)
                elif kpl.jenis_transaksi == u'3' and kpl.nilai <= kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1' and \
                    kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Non Materai) 19')
                    kpl.save()
                    jurnal_pencairan(kpl, request.user)
                elif kpl.jenis_transaksi == u'3' and kpl.nilai <= kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'1' and \
                    kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Non Materai) 20')
                    kpl.save()
                    jurnal_pencairan_nonmaterai(kpl, request.user)
                ####MOBIL ANGGOTA
                elif kpl.jenis_transaksi == u'3' and kpl.nilai >  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2' and \
                    kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Non Materai) 21')
                    kpl.save()
                    jurnal_pencairan_nonanggota(kpl, request.user)
                elif kpl.jenis_transaksi == u'3' and kpl.nilai >  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2' and \
                    kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Non Materai) 22')
                    kpl.save()
                    jurnal_pencairan_nonanggota_nonmaterai(kpl, request.user)
                elif kpl.jenis_transaksi == u'3' and kpl.nilai <=  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2' and \
                    kpl.bea_materai > 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Non Materai) 23')
                    kpl.save()
                    jurnal_pencairan_nonanggota(kpl, request.user)
                elif kpl.jenis_transaksi == u'3' and kpl.nilai <=  kpl.taksir.maxpinjaman and kpl.agnasabah.jenis_keanggotaan == u'2' and \
                    kpl.bea_materai == 0:
                    kpl.nocoa_titipan = '21.05.01'
                    kpl.nocoa_kas = '11.01.04'
                    messages.add_message(request, messages.INFO, 'Jurnal Pencairan Berhasil (Non Anggota) (Non Materai) 24')
                    kpl.save()
                    jurnal_pencairan_nonanggota_nonmaterai(kpl, request.user)
            else:
                messages.add_message(request, messages.INFO,'### PENGAJUAN DITOLAK ###')         
            return HttpResponseRedirect('/')
    else:
        form = KepalaGeraiForm()
    variables = RequestContext(request, {'kpl': kpl, 'form': form})
    template = 'kplgerai/approve_pencairan.html'
    return render_to_response(template, variables)

def approve_gu(request,object_id):
    kpl = AkadGadai.objects.get(id=object_id)
    sekarang= datetime.date.today()
    form = KepalaGeraiForm(initial={'kepala_gerai': kpl.id,'tanggal': sekarang})
    form.fields['kepala_gerai'].widget = forms.HiddenInput()
    template = 'kplgerai/approve_kg_gu.html'
    variable = RequestContext(request, {'kpl': kpl,'form':form})
    return render_to_response(template,variable)
  
def verifikasi_kg_gu(request, object_id):
    kpl = AkadGadai.objects.get(id=object_id)
    if request.method == 'POST':
        form = KepalaGeraiForm(request.POST)
        if form.is_valid():
            kepala_gerai = form.cleaned_data['kepala_gerai']   
            tanggal = form.cleaned_data['tanggal']
            status = form.cleaned_data['status']
            note = form.cleaned_data['note']
            kp_gerai = KepalaGerai(kepala_gerai=kepala_gerai,tanggal=tanggal,status=status,note=note)
            kp_gerai.save()
            materai = Biaya_Materai_Cab(gerai_id = kpl.gerai.id,tanggal=tanggal,nilai=kpl.bea_materai,keterangan='Materai Pencairan',\
               norek= kpl.norek())
            materai.save()
            if kp_gerai.status == '1':
                messages.add_message(request, messages.INFO, '### PENGAJUAN DISIMPAN ###')
            else:
                messages.add_message(request, messages.INFO,' ### PENGAJUAN DITOLAK ###')         
            return HttpResponseRedirect('/')
    else:
        form = KepalaGeraiForm()
    variables = RequestContext(request, {'kpl': kpl, 'form': form})
    template = 'kplgerai/approve_kg_gu.html'
    return render_to_response(template, variables)


def all_transaksi(request):
    akad= AkadGadai.objects.all()
    start_date = None
    end_date = None
    form = AkadGadaiForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l) in akad:
                tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date))
        template='kplgerai/laporan/rekap_all_transaksi.html'
        variable = RequestContext(request,{'tes':tb,
        'form':form,
        'start_date':start_date,
        'end_date':end_date,
        'nilai': sum([b.nilai for b in tb ]),
        'os_pokok': sum([b.os_pokok for b in tb ]),
        'jasa': sum([b.jasa for b in tb ]),
        'adm': sum([b.adm for b in tb ]),
        'simpan': sum([b.biayasimpan for b in tb ]),
        'bersih' : sum([b.jumlah_biaya for b in tb ]),})
        return render_to_response(template,variable)
    
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l) in akad:
                tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date))
        template1='kplgerai/laporan/cetak_all_transaksi.html'
        variable = RequestContext(request,{'tes':tb,
        'form':form,
        'start_date':start_date,
        'end_date':end_date,
        'nilai': sum([b.nilai for b in tb ]),
        'os_pokok': sum([b.os_pokok for b in tb ]),
        'jasa': sum([b.jasa for b in tb ]),
        'adm': sum([b.adm for b in tb ]),
        'simpan': sum([b.biayasimpan for b in tb ]),
        'bersih' : sum([b.jumlah_biaya for b in tb ]),})
        return render_to_response(template1,variable)
        
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l) in akad:
                tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date))
        a = sum([b.nilai for b in tb ])
        c = sum([b.nilai_jasa for b in tb ]) + sum([b.nilai_jasa_kendaraan for b in tb ])
        d = sum([b.nilai_adm for b in tb ]) + sum([b.nilai_adm_kendaraan for b in tb ])
        e = sum([b.biayasimpan for b in tb ]) + sum([b.nilai_beasimpan_kendaraan for b in tb ])
        f = start_date
        g = end_date
        #h = nacab.nama_cabang
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0})
        bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#46D7F4'})
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#46D7F4'})
        merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
        worksheet.set_column(0, 0, 10) 
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 11)
        worksheet.set_column(3, 3, 37)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        worksheet.set_column(7, 7, 10)
        worksheet.set_column(8, 8, 10)
        worksheet.set_column(9, 9, 10)
        worksheet.set_column(10, 10, 10)
        
        
        worksheet.merge_range('A1:K1', 'LAPORAN ALL TRANSAKSI ', merge_format1)
        worksheet.merge_range('A2:K2', 'PERIODE '+ f + " s.d " + g, merge_format1)
        worksheet.merge_range('A4:A5', 'Tanggal Pencairan', merge_format)
        worksheet.merge_range('B4:B5', 'No Rekening', merge_format)
        worksheet.merge_range('C4:C5', 'No Nasabah', merge_format)
        worksheet.merge_range('D4:D5', 'Nama', merge_format)
        worksheet.merge_range('E4:E5', 'JW (hari)', merge_format)
        worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
        worksheet.merge_range('G4:G5', 'Status', merge_format)
        
        worksheet.merge_range('H4:H5', 'Jenis barang', merge_format)
        worksheet.merge_range('I4:I5', 'Nilai', merge_format)
        worksheet.merge_range('J4:L4', 'Pendapatan (Rp)', merge_format)
        worksheet.write('J5', 'Jasa (Rp)',  bold1)
        worksheet.write('K5', 'Adm (Rp)', bold1)
        worksheet.write('L5', 'Bea Simpan (Rp)', bold1)
        #worksheet.write('L2', 'Total', bold)

        row = 5
        col = 0
        for t in tb:
            worksheet.write_datetime(row, col , t.tanggal, date_format )
            worksheet.write_string(row, col + 1 , t.norek() )
            worksheet.write_string(row, col + 2 , t.nonas() )
            worksheet.write_string(row, col + 3 , t.agnasabah.nama )
            worksheet.write_string(row, col + 4, t.jw_all())
            worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
            worksheet.write_string(row, col + 6, t.get_status_transaksi_display())
            worksheet.write_string(row, col + 7, t.get_jenis_transaksi_display())
            worksheet.write_number(row, col + 8, t.nilai, money_format)
            worksheet.write_number(row, col + 9, t.jasa_all(), money_format)
            worksheet.write_number(row, col + 10, t.adm_all(), money_format)
            worksheet.write_number(row, col + 11, t.beasimpan_all(), money_format)
            #worksheet.write_number(row, col + 11, a, money_format)
            #worksheet.write_number  (row, col + 4, t.debet, money_format)
            #worksheet.write_number  (row, col + 5, t.kredit, money_format)
            #worksheet.write_number  (row, col + 6,(t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit),money_format)
            row += 1
        worksheet.write(row, 5, 'Total', bold)    
        worksheet.write(row, 8, a, money_format)
        worksheet.write(row, 9, c, money_format)
        worksheet.write(row, 10, d, money_format)
        worksheet.write(row, 11, e, money_format)
        
        
        
        
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=Laporan_all_transaksi.xlsx"
        return response
        
    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('kplgerai/laporan/rekap_all_transaksi.html', variables)


def pelunasan_gerai(request,object_id):
    nacab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    kocab = object_id
    akad= AkadGadai.objects.all()
    start_date = None
    end_date = None
    form = AkadGadaiForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l) in akad:
                tb = AkadGadai.objects.filter(lunas__isnull =False).filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang = object_id)
        template='kplgerai/laporan/rekap_pelunasan_hari.html'
        variable = RequestContext(request,{'tes':tb,
        'form':form,
        'start_date':start_date,
        'end_date':end_date,
        'kocab':kocab,
        'nacab':nacab,
        'nilai': sum([b.nilai for b in tb ]),
        'jasa': sum([b.jasa for b in tb ]),
        'adm': sum([b.adm for b in tb ]),
        'simpan': sum([b.biayasimpan for b in tb ]),
        'bersih' : sum([b.jumlah_biaya for b in tb ]),})
        return render_to_response(template,variable)
    
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l) in akad:
                tb = AkadGadai.objects.filter(lunas__isnull =False).filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang = object_id)
        template1='kplgerai/laporan/cetak_rekap_pelunasan_hari.html'
        variable = RequestContext(request,{'tes':tb,
        'form':form,
        'start_date':start_date,
        'end_date':end_date,
        'kocab':kocab,
        'nacab':nacab,
        'nilai': sum([b.nilai for b in tb ]),
        'jasa': sum([b.jasa for b in tb ]),
        'adm': sum([b.adm for b in tb ]),
        'simpan': sum([b.biayasimpan for b in tb ]),
        'bersih' : sum([b.jumlah_biaya for b in tb ]),})
        return render_to_response(template1,variable)
        
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l) in akad:
                tb = AkadGadai.objects.filter(lunas__isnull =False).filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang = object_id)
        a = sum([b.nilai for b in tb ])
        c = sum([b.nilai_jasa for b in tb ]) + sum([b.nilai_jasa_kendaraan for b in tb ])
        d = sum([b.nilai_adm for b in tb ]) + sum([b.nilai_adm_kendaraan for b in tb ])
        e = sum([b.biayasimpan for b in tb ]) + sum([b.nilai_beasimpan_kendaraan for b in tb ])
        f = start_date
        g = end_date
        h = nacab.nama_cabang
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0})
        bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#46D7F4'})
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#46D7F4'})
        merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
        worksheet.set_column(0, 0, 10) 
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 11)
        worksheet.set_column(3, 3, 37)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        worksheet.set_column(7, 7, 10)
        worksheet.set_column(8, 8, 10)
        worksheet.set_column(9, 9, 10)
        worksheet.set_column(10, 10, 10)
        
        worksheet.merge_range('A1:K1', 'LAPORAN PELUNASAN '+ h, merge_format1)
        worksheet.merge_range('A2:K2', 'PERIODE '+ f + " s.d " + g, merge_format1)
        worksheet.merge_range('A4:A5', 'Tanggal Pencairan', merge_format)
        worksheet.merge_range('B4:B5', 'No Rekening', merge_format)
        worksheet.merge_range('C4:C5', 'No Nasabah', merge_format)
        worksheet.merge_range('D4:D5', 'Nama', merge_format)
        worksheet.merge_range('E4:E5', 'JW (hari)', merge_format)
        worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
        worksheet.merge_range('G4:G5', 'Jenis barang', merge_format)
        worksheet.merge_range('H4:H5', 'Nilai', merge_format)
        worksheet.merge_range('I4:K4', 'Pendapatan (Rp)', merge_format)
        worksheet.write('I5', 'Jasa (Rp)',  bold1)
        worksheet.write('J5', 'Adm (Rp)', bold1)
        worksheet.write('K5', 'Bea Simpan (Rp)', bold1)

        row = 5
        col = 0
        for t in tb:
            worksheet.write_datetime(row, col , t.tanggal, date_format )
            worksheet.write_string(row, col + 1 , t.norek() )
            worksheet.write_string(row, col + 2 , t.nonas() )
            worksheet.write_string(row, col + 3 , t.agnasabah.nama )
            worksheet.write_string(row, col + 4, t.jw_all())
            worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
            worksheet.write_string(row, col + 6, t.get_jenis_transaksi_display())
            worksheet.write_number(row, col + 7, t.nilai, money_format)
            worksheet.write_number(row, col + 8, t.jasa_all(), money_format)
            worksheet.write_number(row, col + 9, t.adm_all(), money_format)
            worksheet.write_number(row, col + 10, t.beasimpan_all(), money_format)

            row += 1
        worksheet.write(row,4, 'Total', bold)    
        worksheet.write(row,7, a, money_format)
        worksheet.write(row, 8, c, money_format)
        worksheet.write(row, 9, d, money_format)
        worksheet.write(row, 10, e, money_format)
        
        
        
        
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=Laporan_Pelunasan.xlsx"
        return response
        
    else:
        variables = RequestContext(request, {'form': form,'kocab':kocab})
        return render_to_response('kplgerai/laporan/rekap_pelunasan_hari.html', variables)

def pencairan_gerai(request,object_id):
    nacab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    kocab = object_id
    akad= AkadGadai.objects.all()
    start_date = None
    end_date = None
    form = AkadGadaiForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l) in akad:
                tb = AkadGadai.objects.filter(lunas__isnull =True).filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang = object_id)
        template='kplgerai/laporan/rekaphari.html'
        variable = RequestContext(request,{'tes':tb,
        'form':form,
        'start_date':start_date,
        'end_date':end_date,
        'kocab':kocab,
        'nacab':nacab,
        'nilai': sum([b.nilai for b in tb ]),
        'jasa': sum([b.jasa for b in tb ]),
        'adm': sum([b.adm for b in tb ]),
        'simpan': sum([b.biayasimpan for b in tb ]),
        'bersih' : sum([b.jumlah_biaya for b in tb ]),})
        return render_to_response(template,variable)
    
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l) in akad:
                tb = AkadGadai.objects.filter(lunas__isnull =True).filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang = object_id)
        template1='kplgerai/laporan/cetak_rekaphari.html'
        variable = RequestContext(request,{'tes':tb,
        'form':form,
        'start_date':start_date,
        'end_date':end_date,
        'kocab':kocab,
        'nacab':nacab,
        'nilai': sum([b.nilai for b in tb ]),
        'jasa': sum([b.jasa for b in tb ]),
        'adm': sum([b.adm for b in tb ]),
        'simpan': sum([b.biayasimpan for b in tb ]),
        'bersih' : sum([b.jumlah_biaya for b in tb ]),})
        return render_to_response(template1,variable)
        
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l) in akad:
                tb = AkadGadai.objects.filter(lunas__isnull =True).filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang = object_id)
        a = sum([b.nilai for b in tb ])
        c = sum([b.nilai_jasa for b in tb ]) + sum([b.nilai_jasa_kendaraan for b in tb ])
        d = sum([b.nilai_adm for b in tb ]) + sum([b.nilai_adm_kendaraan for b in tb ])
        e = sum([b.biayasimpan for b in tb ]) + sum([b.nilai_beasimpan_kendaraan for b in tb ])
        f = start_date
        g = end_date
        h = nacab.nama_cabang
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0})
        bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#46D7F4'})
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#46D7F4'})
        merge_format1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter',})
        
        worksheet.set_column(0, 0, 10) 
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 11)
        worksheet.set_column(3, 3, 37)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        worksheet.set_column(7, 7, 10)
        worksheet.set_column(8, 8, 10)
        worksheet.set_column(9, 9, 10)
        worksheet.set_column(10, 10, 10)
        
        worksheet.merge_range('A1:K1', 'LAPORAN PENCAIRAN '+ h, merge_format1)
        worksheet.merge_range('A2:K2', 'PERIODE '+ f + " s.d " + g, merge_format1)
        worksheet.merge_range('A4:A5', 'Tanggal Pencairan', merge_format)
        worksheet.merge_range('B4:B5', 'No Rekening', merge_format)
        worksheet.merge_range('C4:C5', 'No Nasabah', merge_format)
        worksheet.merge_range('D4:D5', 'Nama', merge_format)
        worksheet.merge_range('E4:E5', 'JW (hari)', merge_format)
        worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
        worksheet.merge_range('G4:G5', 'Jenis barang', merge_format)
        worksheet.merge_range('H4:H5', 'Nilai', merge_format)
        worksheet.merge_range('I4:K4', 'Pendapatan (Rp)', merge_format)
        worksheet.write('I5', 'Jasa (Rp)',  bold1)
        worksheet.write('J5', 'Adm (Rp)', bold1)
        worksheet.write('K5', 'Bea Simpan (Rp)', bold1)

        row = 5
        col = 0
        for t in tb:
            worksheet.write_datetime(row, col , t.tanggal, date_format )
            worksheet.write_string(row, col + 1 , t.norek() )
            worksheet.write_string(row, col + 2 , t.nonas() )
            worksheet.write_string(row, col + 3 , t.agnasabah.nama )
            worksheet.write_string(row, col + 4, t.jw_all())
            worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
            worksheet.write_string(row, col + 6, t.get_jenis_transaksi_display())
            worksheet.write_number(row, col + 7, t.nilai, money_format)
            worksheet.write_number(row, col + 8, t.jasa_all(), money_format)
            worksheet.write_number(row, col + 9, t.adm_all(), money_format)
            worksheet.write_number(row, col + 10, t.beasimpan_all(), money_format)
            row += 1

        worksheet.write(row,4, 'Total', bold)    
        worksheet.write(row,7, a, money_format)
        worksheet.write(row, 8, c, money_format)
        worksheet.write(row, 9, d, money_format)
        worksheet.write(row, 10, e, money_format)
        
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=Laporan_Pencairan.xlsx"
        return response
        
    else:
        variables = RequestContext(request, {'form': form,'kocab':kocab})
        return render_to_response('kplgerai/laporan/rekaphari.html', variables)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='KPLGERAI'))
def labarugi(request):
    user = request.user
    kocab =  user.profile.gerai.kode_cabang
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    start_date = None
    end_date = None
    id_cabang = None
    akun =[]
    if  'start_date' in request.GET and request.GET['start_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = kocab
        lb_akun = Tbl_Akun.objects.filter(view_unit__in=('300','0')).filter(jenis="l")
        for c in lb_akun :
            akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit(id_cabang,start_date,end_date),'debet':c.my_debet(id_cabang,start_date,end_date),#'saldo_awal':saldo_dk ,
               'coa':c.coa,'id':c.id,'id_cabang':300 + (int(id_cabang)) ,'header_parent':c.header_parent,
               'saldo_akhir': c.view_saldo_akhir(id_cabang,start_date,end_date),
               'saldo_awal': c.saldo_pjb,})
            start_date = start_date
            id_cabang = kocab
            end_date = end_date    

    template='kplgerai/labarugi.html'
    variable = RequestContext(request,{'akun':akun,'total_debet':t_debet,'total_kredit':t_kredit,'total_saldo_akhir':t_saldo_akhir,
        'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date,'kocab':kocab})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KPLGERAI'))
def neraca(request):
    user = request.user
    kocab =  user.profile.gerai.kode_cabang
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    start_date = None
    end_date = None
    id_cabang = None
    akun =[]

    if  'start_date' in request.GET and request.GET['start_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = object_id
        lb_akun = Tbl_Akun.objects.filter(view_unit__in =('0','300')).filter(jenis__in = ('a','p')).order_by('coa')
        for c in lb_akun :
            akun.append({'c':c,'deskripsi':c.deskripsi,
                'kredit':c.my_kredit(id_cabang,start_date,end_date),'debet':c.my_debet(id_cabang,start_date,end_date),
                'coa':c.coa,'id':c.id,'id_cabang':300 + (int(object_id)) ,'header_parent':c.header_parent,
                'saldo_akhir': c.view_saldo_akhir(id_cabang,start_date,end_date),
                'saldo_awal': c.saldo_pjb,})
            t_debet += c.total_debet_nenek(id_cabang,start_date,end_date)
            t_kredit += c.total_kredit_nenek(id_cabang,start_date,end_date)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date

    template='kplgerai/neraca.html'
    variable = RequestContext(request,{'akun':akun,'total_debet':t_debet,'total_kredit':t_kredit,'kocab':kocab,
        'total_saldo_akhir':t_saldo_akhir,'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KPLGERAI'))
def neraca_percobaan(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    kocab = cab
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    start_date = None
    end_date = None
    id_cabang = None
    akun =[]
    if  'start_date' in request.GET and request.GET['start_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = cab
        lb_akun = Tbl_Akun.objects.filter(view_unit__in =('0','300'),jenis__in = ('a','p','l')).order_by('coa')
        for c in lb_akun :
            akun.append({'c':c,'deskripsi':c.deskripsi,
                'kredit':c.my_kredit(id_cabang,start_date,end_date),'debet':c.my_debet(id_cabang,start_date,end_date),
                'coa':c.coa,'id':c.id,'id_cabang':300 + (int(cab)) ,'header_parent':c.header_parent,
                'saldo_akhir': c.view_saldo_akhir(id_cabang,start_date,end_date),
                'saldo_awal': c.saldo_pjb,})
            t_debet += c.total_debet_nenek(id_cabang,start_date,end_date)
            t_kredit += c.total_kredit_nenek(id_cabang,start_date,end_date)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date

        template='kplgerai/neraca_percobaan.html'
        variable = RequestContext(request,{'akun':akun,'total_debet':t_debet,'total_kredit':t_kredit,'kocab':kocab,
            'total_saldo_akhir':t_saldo_akhir,'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
        return render_to_response(template,variable)
    elif  'start_date' in request.GET and request.GET['start_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = object_id
        lb_akun = Tbl_Akun.objects.filter(view_unit__in =('0','300'),jenis__in = ('a','p','l')).order_by('coa')
        for c in lb_akun :
            akun.append({'c':c,'deskripsi':c.deskripsi,
                'kredit':c.my_kredit(id_cabang,start_date,end_date),'debet':c.my_debet(id_cabang,start_date,end_date),
                'coa':c.coa,'id':c.id,'id_cabang':300 + (int(cab)) ,'header_parent':c.header_parent,
                'saldo_akhir': c.view_saldo_akhir(id_cabang,start_date,end_date),
                'saldo_awal': c.saldo_pjb,})
            t_debet += c.total_debet_nenek(id_cabang,start_date,end_date)
            t_kredit += c.total_kredit_nenek(id_cabang,start_date,end_date)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date

        template='kplgerai/neraca_percobaan_pdf.html'
        variable = RequestContext(request,{'akun':akun,'total_debet':t_debet,'total_kredit':t_kredit,'kocab':kocab,
            'total_saldo_akhir':t_saldo_akhir,'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
        return render_to_response(template,variable)
    else:
        variables = RequestContext(request, {'kocab':kocab})
        return render_to_response('kplgerai/neraca_percobaan.html', variables)    

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KPLGERAI'))
def buku_besar_cabang(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    kocab = cab
    ledger = Tbl_Transaksi.objects.all()
    banyak = ledger.all
    start_date = None
    end_date = None
    form = Tbl_AkunForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :   
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        if cab == '0':
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa = l ).filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal =2)
                akumulasi_debet = 0
                akumulasi_kredit = 0
                for t in tb:
                    if t.id_coa.coa[0:2] == str(20) or t.id_coa.coa[0:2] == str(21) or t.id_coa.coa[0:2] == str(22) or t.id_coa.coa[0:2] == str(23) or t.id_coa.coa[0:2] == str(30) or \
                        t.id_coa.coa[0:2] == str(31) or t.id_coa.coa[0:2] == str(32) or t.id_coa.coa[0:2] == str(33) or t.id_coa.coa[0:2] == str(34) or t.id_coa.coa[0:2] == str(35) or \
                        t.id_coa.coa[0:2] == str(40) or t.id_coa.coa[0:2] == str(41) or t.id_coa.coa[0:2] == str(60) or t.id_coa.coa[0:2] == str(61):
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_kredit - akumulasi_debet)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})
                    #all.append(t)
        else:
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa=l).filter(tgl_trans__range=(start_date,end_date)).\
                    filter(id_cabang=cab,status_jurnal = 2)
                akumulasi_debet = 0
                akumulasi_kredit = 0
                for t in tb:
                    if t.id_coa.coa[0:2] == str(20) or t.id_coa.coa[0:2] == str(21) or t.id_coa.coa[0:2] == str(22) or t.id_coa.coa[0:2] == str(23) or t.id_coa.coa[0:2] == str(30) or \
                        t.id_coa.coa[0:2] == str(31) or t.id_coa.coa[0:2] == str(32) or t.id_coa.coa[0:2] == str(33) or t.id_coa.coa[0:2] == str(34) or t.id_coa.coa[0:2] == str(35) or \
                        t.id_coa.coa[0:2] == str(40) or t.id_coa.coa[0:2] == str(41) or t.id_coa.coa[0:2] == str(60) or t.id_coa.coa[0:2] == str(61):
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_kredit - akumulasi_debet)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
                    #all.append(t)
        template='kplgerai/buku_besar_cabang.html'
        variable = RequestContext(request,{'ledger':all,'form':form,'start_date':start_date,'end_date':end_date,'id_cabang':cab})
        return render_to_response(template,variable)

    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        #id_cabang = request.GET['id_cabang']
        if cab == '0':
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa = l ).filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal= 2)
                akumulasi_debet = 0
                akumulasi_kredit = 0
                for t in tb:
                    akumulasi_debet += t.debet
                    akumulasi_kredit += t.kredit
                    all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                    'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                    'id_coa':t.id_coa})
        else:
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa = l).filter(tgl_trans__range=(start_date,end_date))\
                    .filter(id_cabang=cab).filter(status_jurnal=2)
                akumulasi_debet = 0
                akumulasi_kredit = 0
                for t in tb:
                    akumulasi_debet += t.debet
                    akumulasi_kredit += t.kredit
                    all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                    'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                    'id_coa':t.id_coa})
        template='kplgerai/buku_besar_cabang_pdf.html'
        variable = RequestContext(request,{'ledger':all,'form':form,'start_date':start_date,'end_date':end_date,'id_cabang':object_id})
        return render_to_response(template,variable)
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for (l,k) in AKUN:
            tb = Tbl_Transaksi.objects.filter(id_coa = l,tgl_trans__range=(start_date,end_date)).filter(id_cabang=cab).\
                    filter(status_jurnal=2)
            akumulasi_debet = 0
            akumulasi_kredit = 0
            for t in tb:
                all.append(t)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0})
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        worksheet.set_column(0, 0, 10) 
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 11)
        worksheet.set_column(3, 3, 37)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        
        worksheet.write('A1', 'Tanggal', bold)
        worksheet.write('B1', 'Nomor Bukti', bold)
        worksheet.write('C1', 'COA', bold)
        worksheet.write('D1', 'Keterangan', bold)
        worksheet.write('E1', 'Debet', bold)
        worksheet.write('F1', 'Kredit', bold)
        worksheet.write('G1', 'Saldo', bold)        
        row = 1
        col = 0
        for t in all:
            akumulasi_debet += t.debet
            akumulasi_kredit += t.kredit
            worksheet.write_datetime(row, col , t.tgl_trans, date_format )
            worksheet.write_string(row, col + 1 , t.jurnal.nobukti )
            worksheet.write_string(row, col + 2 , t.gabung_kode_coa() )
            worksheet.write_string(row, col + 3 , t.jurnal.diskripsi )
            worksheet.write_number  (row, col + 4, t.debet, money_format)
            worksheet.write_number  (row, col + 5, t.kredit, money_format)
            worksheet.write_number  (row, col + 6,(t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit),money_format)
            row += 1
        worksheet.write(row, 0, 'Total', bold)
        worksheet.write(row, 4, '=SUM(E2:E27)', money_format)
        worksheet.write(row, 5, '=SUM(F2:F27)', money_format)
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=bukubesar_pjb_all).xlsx"
        return response

    else:
        variables = RequestContext(request, {'form': form,'ag':ledger,'kocab':kocab})
        return render_to_response('kplgerai/buku_besar_cabang.html', variables)

@login_required
def list(request,object_id):
    mankeu = Tbl_Transaksi.objects.filter(status_jurnal=1)
    akun=[]
    form = Tbl_AkunForm()
    start_date = None
    end_date = None

    if 'start_date' in request.GET and request.GET['start_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        mankeu = Tbl_Transaksi.objects.filter(id_cabang=object_id).filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal=1)        
        for c in mankeu :
            akun.append(c)
            start_date = start_date
            end_date = end_date
    template = 'kplgerai/approvejurnal.html'
    variables = RequestContext(request, {'mankeu': akun,'form':form,'start_date':start_date,'end_date':end_date,'kocab':object_id,
    'total_debet': sum([p.debet for p in akun]),'total_kredit': sum([p.kredit for p in akun]),})    
    return render_to_response(template, variables)

def approve_kpg_all(request,object_id):
    start_date = datetime.date.today()
    end_date = datetime.date.today()
    for i in request.POST.getlist('id_pilih'):
        gl = Tbl_Transaksi.objects.get(id=int(i))
        id_cabang = gl.id_cabang
        gl.status_jurnal = 2
        #gl.id_coa.saldo_akhir_pjb = gl.id_coa.hitung_saldo_akhir(id_cabang,start_date,end_date)
        gl.id_coa.saldo_akhir_pjb = 10000000
        gl.id_coa.tanggal = start_date
        messages.add_message(request, messages.INFO,' Input GL manual Terposting.')
        gl.save()
        
        man = KplGerai(kpl_gerai = gl,akun_kpl=None,status = u'1',tanggal=datetime.date.today())
        man.save()
    return HttpResponseRedirect("/")


def jurnal_pencairan(ag, user):
    D = decimal.Decimal
    non = PencairanAdmMapper.objects.get(item= u'1')
    a_titipan_pencairan = non.coa1
    a_pinjaman = non.coa2
    a_pdp_adm = non.coa3
    a_pdp_jasa = non.coa4
    a_pdp_bea_simpan = non.coa5
    a_pdp_materai = non.coa6
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),tgl_trans =ag.tanggal,nobukti=ag.norek(),
        kode_cabang = ag.gerai.kode_cabang,object_id=ag.norek_id(),cu = user,mu=user)
     
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = ag.nilai,kredit = 0,
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,
        debet = 0,kredit =  D(float(ag.jasa_all())),
        id_product = '4',status_jurnal ='2',
        id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    #if ag.jenis_transaksi == u'1':  # sesuai Permintaan memo no 136 tgl 16 okt 2017
    if ag.adm_all() != 0:
        jurnal.tbl_transaksi_set.create(
            jenis = 'Pencairan', id_coa = a_pdp_adm,
            debet = 0,kredit = D(float(ag.adm_all())),
            id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
            id_unit= 300)

    if ag.beasimpan_all() != 0:      
        jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
            debet = 0,kredit =  D(float(ag.beasimpan_all())),
            id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_materai,
        debet = 0,kredit =  D(float(ag.bea_materai)),
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        debet = 0 , kredit = round(D(ag.nilai) - D(ag.adm_all()) - ag.jasa_all() - ag.beasimpan_all())-(ag.bea_materai), 
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)    

def jurnal_pencairan_nonmaterai(ag, user):
    D = decimal.Decimal
    non = PencairanAdmMapper.objects.get(item= u'2')
    a_titipan_pencairan = non.coa1
    a_pinjaman = non.coa2
    a_pdp_adm = non.coa3
    a_pdp_jasa = non.coa4
    a_pdp_bea_simpan = non.coa5
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),tgl_trans =ag.tanggal,nobukti=ag.norek(),
        kode_cabang = ag.gerai.kode_cabang,object_id=ag.norek_id(),cu = user,mu=user)
 
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = ag.nilai,kredit = 0,
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,
        debet = 0,kredit =  D(float(ag.jasa_all())),
        id_product = '4',status_jurnal ='2',
        id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    #if ag.jenis_transaksi == u'1': # sesuai Permintaan memo no 136 tgl 16 okt 2017
    if ag.adm_all() != 0:    
        jurnal.tbl_transaksi_set.create(
            jenis = 'Pencairan', id_coa = a_pdp_adm,
            debet = 0,kredit = D(float(ag.adm_all())),
            id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
            id_unit= 300)

    if ag.beasimpan_all() != 0:    
        jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
            debet = 0,kredit =  D(float(ag.beasimpan_all())),
            id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        debet = 0 , kredit = round(D(ag.nilai) - D(ag.adm_all()) - ag.jasa_all() - ag.beasimpan_all())-(ag.bea_materai), 
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)

def jurnal_pencairan_nonanggota(ag, user):
    D = decimal.Decimal
    non = PencairanAdmMapper.objects.get(item= u'3')
    a_titipan_pencairan = non.coa1
    a_pinjaman = non.coa2
    a_pdp_adm = non.coa3
    a_pdp_jasa = non.coa4
    a_pdp_bea_simpan = non.coa5
    a_pdp_materai = non.coa6
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),tgl_trans =ag.tanggal,nobukti=ag.norek(),
        kode_cabang = ag.gerai.kode_cabang,object_id=ag.norek_id(),cu = user,mu=user)
 
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = ag.nilai,kredit = 0,
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,
        debet = 0,kredit =  D(float(ag.jasa_all())),
        id_product = '4',status_jurnal ='2',
        id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    #if ag.jenis_transaksi == u'1': # sesuai Permintaan memo no 136 tgl 16 okt 2017
    if ag.adm_all() != 0:    
        jurnal.tbl_transaksi_set.create(
            jenis = 'Pencairan', id_coa = a_pdp_adm,
            debet = 0,kredit = D(float(ag.adm_all())),
            id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
            id_unit= 300)
    if ag.beasimpan_all() != 0:
        jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
            debet = 0,kredit =  D(float(ag.beasimpan_all())),
            id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_materai,
        debet = 0,kredit =  D(float(ag.bea_materai)),
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        debet = 0 , kredit = round(D(ag.nilai) - D(ag.adm_all()) - ag.jasa_all() - ag.beasimpan_all())-(ag.bea_materai), 
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)


def jurnal_pencairan_nonanggota_nonmaterai(ag, user):
    D = decimal.Decimal
    non = PencairanAdmMapper.objects.get(item= u'4')
    a_titipan_pencairan = non.coa1
    a_pinjaman = non.coa2
    a_pdp_adm = non.coa3
    a_pdp_jasa = non.coa4
    a_pdp_bea_simpan = non.coa5
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),tgl_trans =ag.tanggal,nobukti=ag.norek(),
        kode_cabang = ag.gerai.kode_cabang,object_id=ag.norek_id(),cu = user,mu=user)
 
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = ag.nilai,kredit = 0,
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,
        debet = 0,kredit =  D(float(ag.jasa_all())),
        id_product = '4',status_jurnal ='2',
        id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    #if ag.jenis_transaksi == u'1': # sesuai Permintaan memo no 136 tgl 16 okt 2017
    if ag.adm_all() != 0:
        jurnal.tbl_transaksi_set.create(
            jenis = 'Pencairan', id_coa = a_pdp_adm,
            debet = 0,kredit = D(float(ag.adm_all())),
            id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
            id_unit= 300)
    if ag.beasimpan_all() !=0 :          
        jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
            debet = 0,kredit =  D(float(ag.beasimpan_all())),
            id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        debet = 0 , kredit = round(D(ag.nilai) - D(ag.adm_all()) - ag.jasa_all() - ag.beasimpan_all())-(ag.bea_materai), 
        id_product = '4',status_jurnal ='2',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
