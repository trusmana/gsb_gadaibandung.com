from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import date_based
from django.http import HttpResponseRedirect
from gadai.appgadai.models import *
from gadai.appgadai.parameterjurnal.forms import BiayaMapperForm,PenKasBankMapperForm,MateraiMapperForm
from django.contrib import messages
from django.views.generic.edit import FormView

def jurnal_panjar(request):
    biaya = PenKasBankMapper.objects.all()
    variables = RequestContext(request, { 'biaya': biaya})
    return render_to_response('keuangan/parameter/show_panjar.html', variables)

def add_panjar(request):
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
            return HttpResponseRedirect('/parameterjurnal/jurnal_panjar/')
    else:
        f = PenKasBankMapperForm()
    variables = RequestContext(request, { 'form': f })
    return render_to_response('keuangan/parameter/add_panjar.html', variables)

def jurnal_biaya(request):
    biaya = BiayaMapper.objects.all().order_by('item')
    variables = RequestContext(request, { 'biaya': biaya})
    return render_to_response('keuangan/parameter/show.html', variables)

def hapus_jurnal(request,object_id):
    tbl = BiayaMapper.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect('/parameterjurnal/jurnal_biaya/')
    
def edit(request,object_id):
    bak= BiayaMapper.objects.get(id=object_id)
    template='keuangan/parameter/edit.html'
    variable = RequestContext(request,{'tak': bak})
    return HttpResponseRedirect(ag.get_absolute_url())
    
def add(request):
    if request.method == 'POST':
        f = BiayaMapperForm(request.POST)
        if f.is_valid():
            item = f.cleaned_data['item']
            coa = f.cleaned_data['coa']
            cabang = f.cleaned_data['cabang']
            
            f.save()
            messages.add_message(request, messages.INFO,"TAMBAH PARAMETER JURNAL BERHASIL.")
            return HttpResponseRedirect('/parameterjurnal/jurnal_biaya/')
    else:
        f = BiayaMapperForm()
    variables = RequestContext(request, { 'form': f })
    return render_to_response('keuangan/parameter/add.html', variables)

def add_parameter_materai(request):
    if request.method == 'POST':
        f = MateraiMapperForm(request.POST)
        if f.is_valid():
            item = f.cleaned_data['item']
            coa1 = f.cleaned_data['coa1']
            coa2 = f.cleaned_data['coa2']
            coa3 = f.cleaned_data['coa3']
            coa4 = f.cleaned_data['coa4']
            cabang = f.cleaned_data['cabang']

            f.save()
            messages.add_message(request, messages.INFO,"TAMBAH PARAMETER JURNAL MATERAI BERHASIL.")
            return HttpResponseRedirect('/parameterjurnal/jurnal_materai/')
    else:
        f = MateraiMapperForm()
    variables = RequestContext(request, { 'form': f })
    return render_to_response('keuangan/parameter/add_materai.html', variables)

def jurnal_materai(request):
    materai = MateraiMapper.objects.all().order_by('item')
    variables = RequestContext(request, { 'materai': materai})
    return render_to_response('keuangan/parameter/show_materai.html', variables)

def hapus_jurnal_materai(request,object_id):
    mtr = MateraiMapper.objects.get(id=object_id)
    mtr.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Materai Berhasil')
    return HttpResponseRedirect('/parameterjurnal/jurnal_materai/')

def edit_materai(request,object_id):
    bak= MateraiMapper.objects.get(id=object_id)
    template='keuangan/parameter/edit_materai.html'
    variable = RequestContext(request,{'tak': bak})
    return HttpResponseRedirect(ag.get_absolute_url())
