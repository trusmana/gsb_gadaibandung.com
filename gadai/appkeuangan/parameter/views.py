from django.shortcuts import render_to_response, get_object_or_404,render,redirect
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
import datetime
from gadai.appkeuangan.parameter.forms import *
from gadai.appgadai.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta 

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['KEUANGAN','SUPERUSER','MANKEU','KEUANGAN_PJB'])
@login_required


@user_passes_test(is_in_multiple_groups)
def edit_aydamapper(request,object_id):
    post = get_object_or_404(AydaMapper, id=object_id)
    if request.method == "POST":
        form = AydaMapperForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/aydamapper/')
    else:
        form = AydaMapperForm(instance=post)
    return render(request, 'parameter/edit_aydamapper.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def aydamapper(request):
    sekarang = datetime.date.today()
    gu = AydaMapper.objects.all()
    if request.POST:
        form = AydaMapperForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Ayda Berhasil")
            return HttpResponseRedirect('/parameter/aydamapper/')
    else:
        form = AydaMapperForm()
    template = 'parameter/aydamapper.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)


@login_required
@user_passes_test(is_in_multiple_groups)
def edit_rak_kasir_plns(request,object_id):
    post = get_object_or_404(KasirPelunasanRakMapper, id=object_id)
    if request.method == "POST":
        form = KasirPelunasanRakMapperForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/rak_kasir_plns/')
    else:
        form = KasirPelunasanRakMapperForm(instance=post)
    return render(request, 'parameter/edit_rak_plns.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def rak_kasir_plns(request):
    sekarang = datetime.date.today()
    gu = KasirPelunasanRakMapper.objects.all().order_by('id')
    if request.POST:
        form = KasirPelunasanRakMapperForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/rak_kasir_plns/')
    else:
        form = KasirPelunasanRakMapperForm()
    template = 'parameter/rak_kasir_plns.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_rak_pusat(request,object_id):
    post = get_object_or_404(RakPusatMapper, id=object_id)
    if request.method == "POST":
        form = RakPusatMapperForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/rak_pusat/')
    else:
        form = RakPusatMapperForm(instance=post)
    return render(request, 'parameter/edit_rak_pusat.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def rak_pusat(request):
    sekarang = datetime.date.today()
    gu = RakPusatMapper.objects.all().order_by('id')
    if request.POST:
        form = RakPusatMapperForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/rak_pusat/')
    else:
        form = RakPusatMapperForm()
    template = 'parameter/rak_pusat.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_biaya_pusat(request,object_id):
    post = get_object_or_404(BiayaPusatMapper, id=object_id)
    if request.method == "POST":
        form = BiayaPusatMapperForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/biaya_pusat/')
    else:
        form = BiayaPusatMapperForm(instance=post)
    return render(request, 'parameter/edit_biaya_pusat.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def biaya_pusat(request):
    sekarang = datetime.date.today()
    gu = BiayaPusatMapper.objects.all().order_by('id')
    if request.POST:
        form = BiayaPusatMapperForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/biaya_pusat/')
    else:
        form = BiayaPusatMapperForm()
    template = 'parameter/biaya_pusat.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_materai_pusat(request,object_id):
    post = get_object_or_404(MateraiPusatMapper, id=object_id)
    if request.method == "POST":
        form = MateraiPusatForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/materai_pusat/')
    else:
        form = MateraiPusatForm(instance=post)
    return render(request, 'parameter/edit_materai_pusat.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def materai_pusat(request):
    sekarang = datetime.date.today()
    gu = MateraiPusatMapper.objects.all().order_by('id')
    if request.POST:
        form = MateraiPusatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/materai_pusat/')
    else:
        form = MateraiPusatForm()
    template = 'parameter/materai_pusat.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_materai_mapper(request,object_id):
    post = get_object_or_404(MateraiMapper, id=object_id)
    if request.method == "POST":
        form = MateraiForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/materai_mapper/')
    else:
        form = MateraiForm(instance=post)
    return render(request, 'parameter/edit_materai_mapper.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def materai_mapper(request):
    sekarang = datetime.date.today()
    gu = MateraiMapper.objects.all().order_by('id')
    if request.POST:
        form = MateraiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/materai_mapper/')
    else:
        form = MateraiForm()
    template = 'parameter/materai_mapper.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_uangmuka_gerai(request,object_id):
    post = get_object_or_404(UangMukaGeraiMapper, id=object_id)
    if request.method == "POST":
        form = UangMukaForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/uangmuka_gerai/')
    else:
        form = UangMukaForm(instance=post)
    return render(request, 'parameter/edit_uangmuka_gerai.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def uangmuka_gerai(request):
    sekarang = datetime.date.today()
    gu = UangMukaGeraiMapper.objects.all().order_by('id')
    if request.POST:
        form = UangMukaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/uangmuka_gerai/')
    else:
        form = UangMukaForm()
    template = 'parameter/uangmuka_gerai.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_manage_akun(request,object_id):
    post = get_object_or_404(Tbl_Akun, id=object_id)
    if request.method == "POST":
        form = AkunForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/manage_akun/')
    else:
        form = AkunForm(instance=post)
    return render(request, 'parameter/edit_manage_akun.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def manage_akun(request):
    sekarang = datetime.date.today()
    gu = Tbl_Akun.objects.all()
    if request.POST:
        form = AkunForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/manage_akun/')
    else:
        form = AkunForm()
    template = 'parameter/manage_akun.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_pelunasan_kasir(request,object_id):
    post = get_object_or_404(KasirPelunasanMapper, id=object_id)
    if request.method == "POST":
        form = KasirPelunasanMapperForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/jurnal_pelunasan_kasir/')
    else:
        form = KasirPelunasanMapperForm(instance=post)
    return render(request, 'parameter/edit_pelunasan_kasir.html', {'form': form,'id':object_id}) 

@user_passes_test(is_in_multiple_groups)
def jurnal_pelunasan_kasir(request):
    pnkb = KasirPelunasanMapper.objects.all().order_by('item')
    if request.method == 'POST':
        f = KasirPelunasanMapperForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO,"TAMBAH JURNAL PENJUALAN BERHASIL.")
            return HttpResponseRedirect('/parameter/jurnal_pelunasan_kasir/')
    else:
        f = KasirPelunasanMapperForm()
    variables = RequestContext(request, { 'pnkb': pnkb,'form':f})
    return render_to_response('parameter/pelunasan_kasir_mapper.html', variables)

@user_passes_test(is_in_multiple_groups)
def edit_jurnal_pelunasan_adm(request,object_id):
    post = get_object_or_404(AdmPelunasanMapper, id=object_id)
    if request.method == "POST":
        form = AdmPelunasanForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/jurnal_pelunasan_adm/')
    else:
        form = AdmPelunasanForm(instance=post)
    return render(request, 'parameter/edit_jurnal_pelunasan_adm.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def jurnal_pelunasan_adm(request):
    sekarang = datetime.date.today()
    gu = AdmPelunasanMapper.objects.all()
    if request.POST:
        form = AdmPelunasanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/jurnal_pelunasan_adm/')
    else:
        form = AdmPelunasanForm()
    template = 'parameter/jurnal_pelunasan_adm.html'
    variable = RequestContext(request, {'form': form,'pnkb':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_pencairan_adm(request,object_id):
    post = get_object_or_404(PencairanAdmMapper, id=object_id)
    if request.method == "POST":
        form = AdmPencairanForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/pencairan_adm/')
    else:
        form = AdmPencairanForm(instance=post)
    return render(request, 'parameter/edit_pencairan_adm.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def pencairan_adm(request):
    sekarang = datetime.date.today()
    gu = PencairanAdmMapper.objects.all()
    if request.POST:
        form = AdmPencairanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/pencairan_adm/')
    else:
        form = AdmPencairanForm()
    template = 'parameter/pencairan_adm.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_gadai_ulang_adm(request,object_id):
    post = get_object_or_404(AdmGadaiUlangMapper, id=object_id)
    if request.method == "POST":
        form = AdmGadaiUlangForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/gadai_ulang_adm/')
    else:
        form = AdmGadaiUlangForm(instance=post)
    return render(request, 'parameter/edit_gadai_ulang_adm.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def gadai_ulang_adm(request):
    sekarang = datetime.date.today()
    gu = AdmGadaiUlangMapper.objects.all()
    if request.POST:
        form = AdmGadaiUlangForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/gadai_ulang_adm/')
    else:
        form = AdmGadaiUlangForm()
    template = 'parameter/gadai_ulang_adm.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_penjualan_barang(request,object_id):
    post = get_object_or_404(GeraiPenjualanMapper, id=object_id)
    if request.method == "POST":
        form = GeraiPenjualanMapperForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/jurnal_penjualan_barang/')
    else:
        form = GeraiPenjualanMapperForm(instance=post)
    return render(request, 'parameter/edit_penjualan_barang.html', {'form': form,'id':object_id}) 

@user_passes_test(is_in_multiple_groups)
def jurnal_penjualan_barang(request):
    pnkb = GeraiPenjualanMapper.objects.all().order_by('id')
    if request.method == 'POST':
        f = GeraiPenjualanMapperForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO,"TAMBAH JURNAL PENJUALAN BERHASIL.")
            return HttpResponseRedirect('/parameter/jurnal_penjualan_barang/')
    else:
        f = GeraiPenjualanMapperForm()
    variables = RequestContext(request, { 'pnkb': pnkb,'form':f})
    return render_to_response('parameter/show_penjualan_gerai.html', variables)

@user_passes_test(is_in_multiple_groups)
def edit_pnks(request,object_id):
    post = get_object_or_404(PenKasBankMapper, id=object_id)
    if request.method == "POST":
        form = PnkbMapperForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/jurnal_penambahan_kas_bank/')
    else:
        form = PnkbMapperForm(instance=post)
    return render(request, 'parameter/edit_pnks.html', {'form': form,'id':object_id}) 

@user_passes_test(is_in_multiple_groups)
def jurnal_penambahan_kas_bank(request):
    biaya = PenKasBankMapper.objects.all().order_by('id')
    if request.method == 'POST':
        f = PnkbMapperForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO,"TAMBAH PARAMETER JURNAL KAS/BANK BERHASIL.")
            return HttpResponseRedirect('/parameter/jurnal_penambahan_kas_bank/')
    else:
        f = PnkbMapperForm()
    variables = RequestContext(request, { 'pnkb': biaya,'form':f})
    return render_to_response('parameter/show_penambahan_kas_bank.html', variables)

@user_passes_test(is_in_multiple_groups)
def edit_jurnal_kas_bank(request,object_id):
    post = get_object_or_404(PusatKasBankMapper, id=object_id)
    if request.method == "POST":
        form = PusatKasBankMapperForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/jurnal_pusat_kas_bank/')
    else:
        form = PusatKasBankMapperForm(instance=post)
    return render(request, 'parameter/edit_pusat_kas_bank.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def jurnal_pusat_kas_bank(request):
    biaya = PusatKasBankMapper.objects.all()
    if request.method == 'POST':
        f = PusatKasBankMapperForm(request.POST)
        if f.is_valid():
            #item = f.cleaned_data['item']
            #coa = f.cleaned_data['coa']
            #cabang = f.cleaned_data['cabang']

            f.save()
            messages.add_message(request, messages.INFO,"TAMBAH PARAMETER JURNAL PUSAT KAS/BANK BERHASIL.")
            return HttpResponseRedirect('/parameter/jurnal_pusat_kas_bank/')
    else:
        f = PusatKasBankMapperForm()
    variables = RequestContext(request, { 'biaya': biaya,'form':f})
    return render_to_response('parameter/show_pusat_kas_bank.html', variables)

@user_passes_test(is_in_multiple_groups)
def edit_biaya(request,object_id):
    post = get_object_or_404(BiayaMapper, id=object_id)
    if request.method == "POST":
        form = BiayaMapperForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/jurnal_biaya/')
    else:
        form = BiayaMapperForm(instance=post)
    return render(request, 'parameter/edit_biaya.html', {'form': form,'id':object_id}) 
    
@user_passes_test(is_in_multiple_groups)
def hapus_jurnal_biaya(request,object_id):
    tbl = BiayaMapper.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect('/parameter/jurnal_biaya/')

@user_passes_test(is_in_multiple_groups)
def jurnal_biaya(request):
    biaya = BiayaMapper.objects.all().order_by('item')
    if request.method == 'POST':
        f = BiayaMapperForm(request.POST)
        if f.is_valid():
            item = f.cleaned_data['item']
            coa = f.cleaned_data['coa']
            cabang = f.cleaned_data['cabang']
            
            f.save()
            messages.add_message(request, messages.INFO,"TAMBAH PARAMETER JURNAL BERHASIL.")
            return HttpResponseRedirect('/parameter/jurnal_biaya/')
    else:
        f = BiayaMapperForm()
    variables = RequestContext(request, { 'biaya': biaya,'form':f})
    return render_to_response('parameter/show_biaya.html', variables)

@user_passes_test(is_in_multiple_groups)
def jurnal_panjar(request):
    biaya = PenKasBankMapper.objects.all()
    variables = RequestContext(request, { 'biaya': biaya})
    if request.method == 'POST':
        f = PenKasBankMapperForm(request.POST)
        if f.is_valid():
            item = f.cleaned_data['item']
            jenis = f.cleaned_data['jenis']
            coa = f.cleaned_data['coa']
            coa_kredit = f.cleaned_data['coa_kredit']
            cabang = f.cleaned_data['cabang']
            ke_cabang = f.cleaned_data['ke_cabang']

            f.save()
            messages.add_message(request, messages.INFO,"TAMBAH PARAMETER JURNAL BERHASIL.")
            return HttpResponseRedirect('/parameter/jurnal_panjar/')
    else:
        f = PenKasBankMapperForm()
    variables = RequestContext(request, { 'form': f ,'biaya': biaya})
    return render_to_response('parameter/show_panjar.html', variables)

@user_passes_test(is_in_multiple_groups)
def hapus_jurnal(request,object_id):
    tbl = PenKasBankMapper.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect('/parameter/jurnal_panjar/')

@user_passes_test(is_in_multiple_groups)
def edit(request,object_id):
    post = get_object_or_404(GadaiUlangMapper, id=object_id)
    if request.method == "POST":
        form = GadaiUlangForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/gadai_ulang/')
    else:
        form = GadaiUlangForm(instance=post)
    return render(request, 'parameter/edit.html', {'form': form,'id':object_id}) 

@user_passes_test(is_in_multiple_groups)
def gadai_ulang(request):
    sekarang = datetime.date.today()
    gu = GadaiUlangMapper.objects.all()
    if request.POST:
        form = GadaiUlangForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/gadai_ulang/')
    else:
        form = GadaiUlangForm()
    template = 'parameter/gadai_ulang.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_pencairan_kasir(request,object_id):
    post = get_object_or_404(KasirPencairanMapper, id=object_id)
    if request.method == "POST":
        form = KasirPencairanForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/pencairan_kasir/')
    else:
        form = KasirPencairanForm(instance=post)
    return render(request, 'parameter/edit_pencairan_kasir.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def pencairan_kasir(request):
    sekarang = datetime.date.today()
    gu = KasirPencairanMapper.objects.all()
    if request.POST:
        form = KasirPencairanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/pencairan_kasir/')
    else:
        form = KasirPencairanForm()
    template = 'parameter/pencairan_kasir.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

@user_passes_test(is_in_multiple_groups)
def edit_pencairan_kasir_bank(request,object_id):
    post = get_object_or_404(KasirPencairanBankMapper, id=object_id)
    if request.method == "POST":
        form = KasirPencairanBankForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/parameter/pencairan_kasir_bank/')
    else:
        form = KasirPencairanBankForm(instance=post)
    return render(request, 'parameter/edit_pencairan_kasir_bank.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
def pencairan_kasir_bank(request):
    sekarang = datetime.date.today()
    gu = KasirPencairanBankMapper.objects.all()
    if request.POST:
        form = KasirPencairanBankForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Mapper Berhasil")
            return HttpResponseRedirect('/parameter/pencairan_kasir_bank/')
    else:
        form = KasirPencairanBankForm()
    template = 'parameter/pencairan_kasir_bank.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)
