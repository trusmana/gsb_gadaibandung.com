from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import date_based
from django.http import HttpResponseRedirect

from gadai.appgadai.models import MutasiKas, KasBank
from gadai.appgadai.kas.forms import FormPindahbuku, MutasiKasForm

def rekening_show(request, object_id):
    '''
    Tampilkan ringkasan rekening terpilih
    '''
    kasbank = KasBank.objects.get(id=object_id)
    variables = RequestContext(request, {'object_list': kasbank.mutasikas_set.all(), 'kasbank': kasbank})
    
    return render_to_response('kas/kasbank_show.html', variables)

def mutasikas_add(request):
    '''
    Fungsi menambah data MutasiKas
    '''
    if request.method == 'POST':
        f = MutasiKasForm(request.POST)
        if f.is_valid():
            kredit = f.cleaned_data['pengeluaran']
            nilai = f.cleaned_data['nilai']
            if kredit: nilai = -1 * f.cleaned_data['nilai']
            mk = f.save(commit=False)
            mk.nilai = nilai
            mk.save()
            request.user.message_set.create(message="Mutasi kas telah disimpan.")
            return HttpResponseRedirect('/kas/')
    else:
        f = MutasiKasForm()
    variables = RequestContext(request, { 'form': f })
    return render_to_response('kas/mutasikas_form.html', variables)

def mutasikas_bulan(request, tahun, bulan):
    '''
    Fungsi untuk menampilkan mutasi kas dalm periode bulan, tahun terpilih
    '''
    mutasikas_list = MutasiKas.objects.filter(tanggal__year=tahun).filter(tanggal__month=bulan)
    variables = RequestContext(request, {'object_list': mutasikas_list})
    return render_to_response('kas/mutasikas_bulan.html', variables)

def rekening_pindahbuku(request):
    '''Proses pemindahbukuan'''
    if request.method == 'POST':
        f = FormPindahbuku(request.POST)
        if f.is_valid():
            rekening_asal = f.cleaned_data['rekening_asal']
            rekening_tujuan = f.cleaned_data['rekening_tujuan']
            nilai = f.cleaned_data['nilai']
            tanggal = f.cleaned_data['tanggal']
            keterangan = f.cleaned_data['keterangan']
            nobukti = f.cleaned_data['nomor']
            if rekening_asal is not rekening_tujuan:
                mk_asal = MutasiKas(kasbank=rekening_asal, \
                    nilai=-1*nilai, tanggal=tanggal, \
                    keterangan=keterangan, nobukti=nobukti)
                mk_asal.save()
                mk_tujuan = MutasiKas(kasbank=rekening_tujuan, \
                    nilai=nilai, tanggal=tanggal, \
                    keterangan=keterangan, nobukti=nobukti)
                mk_tujuan.save()
                return HttpResponseRedirect('/kas/')
    else:
        f = FormPindahbuku()
    variables = RequestContext(request, {'form': f})
    return render_to_response('kas/rekening_pindahbuku.html', variables)

