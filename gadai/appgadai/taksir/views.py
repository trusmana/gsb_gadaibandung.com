from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,render,redirect
from django import forms
from gadai.appgadai.models import *
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.taksir.forms import TaksirForm,TaksirEditForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required, user_passes_test

def list(request):
    taksir = Taksir.objects.all().order_by('-tglupdate')
    paginator = Paginator(taksir, 20)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        taksir = paginator.page(page)
    except (EmptyPage, InvalidPage):
        taksir = paginator.page(paginator.num_pages)

    template='taksir/index.html'
    variable = RequestContext(request,{'taksir': taksir})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('manop','asmanpjb','staffops')))
def add(request):
    if request.method == "POST":
        form = TaksirForm(request.POST)

        if form.is_valid():
            type = form.cleaned_data['type']
            spesifikasi = form.cleaned_data['spesifikasi']
            harga_baru = form.cleaned_data['harga_baru']
            harga_pasar = form.cleaned_data['harga_pasar']
            maxpinjaman = form.cleaned_data['maxpinjaman']
            tglupdate = form.cleaned_data['tglupdate']
            status = form.cleaned_data['status']
            tks= Taksir (type=type,spesifikasi=spesifikasi,harga_baru=harga_baru,harga_pasar=harga_pasar,maxpinjaman=maxpinjaman,tglupdate=tglupdate,\
                status=status)
            tks.save()
            return HttpResponseRedirect('/taksir/')
    else:
        form = TaksirForm()
    variables = RequestContext(request,{'form':form})
    return render_to_response('taksir/add.html',variables)


def show(request,object_id):
    tkr=Taksir.objects.get(id=object_id)
    template='taksir/show.html'
    variable = RequestContext(request,{'tkr': tkr})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('manop','staffops')))
def edit(request,object_id):
    user = request.user
    sekarang1 = datetime.datetime.now()
    post = get_object_or_404(Taksir, id=object_id)
    taksir=Taksir.objects.get(id=object_id)
    if request.method == "POST":
        form = TaksirEditForm(request.POST, instance=post)
        if form.is_valid():
            historitaksir =  TaksirHistory(history = taksir,type =taksir.type,spesifikasi =taksir.spesifikasi,\
                harga_baru =taksir.harga_baru, harga_pasar =taksir.harga_pasar, maxpinjaman =taksir.maxpinjaman,\
                tglupdate = sekarang1, tgl= sekarang1, status =taksir.status,cu =user,mu = user)
            historitaksir.save()
            post.save()
            return HttpResponseRedirect("/taksir/")
    else:
        form = TaksirEditForm(instance=post)
    return render(request, 'taksir/edit.html', {'form': form,'id':object_id}) 

#def edit(request,object_id):
    #tak=Taksir.objects.get(id=object_id)
    #template='taksir/edit.html'
    #variable = RequestContext(request,{'tak': tak})
    #return render_to_response(template,variable)
    

def cari(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        taksir = Taksir.objects.filter(type__icontains=q)
        return render_to_response('taksir/search.html',
            {'taksir': taksir, 'query': q})
    else:
        return render_to_response('taksir/index.html', {'error': True})
'''
@login_required
@user_passes_test(lambda u: u.groups.filter(name='manop'))
def delete(request, object_id):
    hapus = Taksir.objects.get(id = object_id)
    hapus.delete()    
    return HttpResponseRedirect("/taksir/%s/" % (taksir.id))
'''
