from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,render,redirect
from django import forms
from gadai.appgadai.models import *
from gadai.appgadai.nasabah.form import NasabahForm,EditBarangGuForm,EditParamForm,EditNasabahForm,BlacklistForm,EditNasabahGeraiForm
from gadai.appgadai.akadgadai.forms import AkadForm
from gadai.appgadai.templatetags.number_format import number_format
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['manop','ADMIN','staffops'])

@login_required
def blacklist_edit(request,object_id):
    form = BlacklistForm(request.POST)
    n=Nasabah.objects.get(id=object_id)
    template='nasabah/edit_black_list.html'
    variable = RequestContext(request,{'n': n,'form':form})
    return render_to_response(template,variable)

@login_required
def input_blacklist(request, object_id):
    user = request.user
    n=Nasabah.objects.get(id=object_id)
    if request.method == 'POST':
        f = BlacklistForm(request.POST)
        if f.is_valid():
            status_nasabah = f.cleaned_data['status_nasabah']

            n.status_nasabah  = status_nasabah
            n.save()
            messages.add_message(request, messages.INFO,'### Data Telah Ubah ###.')

            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request,{ 'form': f})
            return render_to_response('nasabah/edit_black_list.html', variables)
    else:
        form  = BlacklistForm()
    variables = RequestContext(request, {'form': form,'n':n,})
    return render_to_response('nasabah/edit_black_list.html', variables)

@login_required
@user_passes_test(is_in_multiple_groups)
def edit_nasabah(request,object_id,akad):
    post = get_object_or_404(Nasabah, id=object_id)
    akadgadai = akad
    if request.method == "POST":
        form = EditNasabahForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/akadgadai/%s/show/' %akad )
    else:
        form = EditNasabahForm(instance=post)
    return render(request, 'nasabah/edit.html', {'form': form,'id':object_id})

@login_required
def edit_nasabahgerai(request,object_id,akad):
    post = get_object_or_404(Nasabah, id=object_id)
    akadgadai = akad
    if request.method == "POST":
        form = EditNasabahGeraiForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            messages.add_message(request, messages.INFO,'### Data Telah Ubah ###.')
            return HttpResponseRedirect('/akadgadai/%s/show/' %akad )
    else:
        form = EditNasabahGeraiForm(instance=post)
    return render(request, 'nasabah/edit_nasabah_gerai.html', {'form': form,'id':object_id,'akad':akad})

@login_required
def history_gu(request,object_id):
    barang = Barang.objects.get(id=object_id)
    history = HistoryAkadUlang.objects.filter(id_barang=barang.id)
    template = 'nasabah/history_gu.html'
    variable = RequestContext(request,{'bar': barang,'history':history})
    return render_to_response(template,variable)

@login_required
def edit_barang(request,object_id):
    barang = Barang.objects.get(id=object_id)
    ak = barang.akadgadai_set.all()
    akad = ak[0]
    
    sekarang = datetime.datetime.now()
    form = EditBarangGuForm(initial={'jenis_barang':barang,'akad_ulang':barang.akad_ulang})
    template = 'nasabah/edit_barang.html'
    variable = RequestContext(request,{'form':form,'bar': barang,'akad':akad})
    return render_to_response(template,variable)

@login_required
def input_edit_history_gu(request, object_id):
    user = request.user
    barang = Barang.objects.get(id=object_id)
    ak = barang.akadgadai_set.all()
    akad = ak[0]
    if request.method == 'POST':
        f = EditBarangGuForm(request.POST)
        if f.is_valid():
            buka_akad_ulang = f.cleaned_data['buka_akad_ulang']
            barang.buka_tutup_gu  = buka_akad_ulang
            #barang.akad_ulang  = buka_akad_ulang
            barang.save()
            messages.add_message(request, messages.INFO,'### Data Telah Ubah ###.')

            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request,{ 'form': f})
            return render_to_response('nasabah/edit_barang.html', variables)
    else:
        form  = EditBarangGuForm()
    variables = RequestContext(request, {'form': form,'barang':barang,})
    return render_to_response('nasabah/edit_barang.html', variables)

@login_required
def list_param(request):
    nsb= ParameterAkadUlang.objects.all()
    #form = AkadForm(initial={'agnasabah': nsb.id,'gerai':nsb.geraigadai,'barang':nsb.baranggerai()})
    #form.fields['agnasabah'].widget = forms.HiddenInput()
    template='nasabah/list_param.html'
    variable = RequestContext(request, {'param': nsb })
    return render_to_response(template, variable)

@login_required
def edit_param(request,object_id):
    nsb= ParameterAkadUlang.objects.get(id = object_id)
   
    sekarang = datetime.datetime.now()
    form = EditParamForm(initial={'jml_akad':nsb.jml_akad, 'tanggal':nsb.tanggal, 'aktif':nsb.aktif})
    template = 'nasabah/edit_param.html'
    variable = RequestContext(request,{'form':form,'nsb':nsb})
    return render_to_response(template,variable)

@login_required
def input_edit_param(request, object_id):
    user = request.user
    nsb= ParameterAkadUlang.objects.get(id = object_id)

    if request.method == 'POST':
        f = EditParamForm(request.POST)
        if f.is_valid():
            jml_akad = f.cleaned_data['jml_akad']
            tanggal = f.cleaned_data['tanggal']
            aktif =  f.cleaned_data['aktif']
 
            nsb.jml_akad = jml_akad
            nsb.tanggal = tanggal
            nsb.aktif =  aktif
            nsb.save()
            messages.add_message(request, messages.INFO,'### DATA Telah Di Edit ###.')

            return HttpResponseRedirect('/nasabah/list_param/')
        else:
            variables = RequestContext(request,{ 'form': form})
            return render_to_response('nasabah/edit_param.html', variables)
    else:
        form  = EditParamForm()
    variables = RequestContext(request, {'form': form,'nsb':nsb})
    return render_to_response('nasabah/edit_param.html', variables)

@login_required
def add_param(request):
    user = request.user
    nsb= ParameterAkadUlang.objects.all()

    if request.method == 'POST':
        f = EditParamForm(request.POST)
        if f.is_valid():
            jml_akad = f.cleaned_data['jml_akad']
            tanggal = f.cleaned_data['tanggal']
            aktif =  f.cleaned_data['aktif']
 
            f = ParameterAkadUlang(jml_akad = jml_akad,tanggal = tanggal,aktif =  aktif)
            f.save()
            messages.add_message(request, messages.INFO,'### DATA Telah Di Tambah ###.')

            return HttpResponseRedirect('/nasabah/list_param/')
        else:
            variables = RequestContext(request,{ 'form': form})
            return render_to_response('nasabah/add_param.html', variables)
    else:
        form  = EditParamForm()
    variables = RequestContext(request, {'form': form,'nsb':nsb})
    return render_to_response('nasabah/add_param.html', variables)


@login_required(login_url='/accounts/login/')
def show(request,object_id):
    #parameter = ParameterAkadUlang.objects.filter(aktif=2)
    #param = parameter[0]
    nsb=Nasabah.objects.get(id=object_id)
    ag=nsb.akadgadai_set.all()
    p=ag.order_by('-tanggal')
    template='nasabah/show.html'
    variable = RequestContext(request,{'nsb': nsb, 'ag':p})#,'param':param})
    return render_to_response(template,variable)

@login_required
def addnasabah(request,object_id):
	sekarang = datetime.date.today()
	nsb=Nasabah.objects.get(id=object_id)
	form = AkadForm(initial={'agnasabah': nsb.id,'gerai':nsb.geraigadai,'barang':nsb.baranggerai(),'tanggal':sekarang})
	form.fields['agnasabah'].widget = forms.HiddenInput()
	template='nasabah/addnasabah.html'
	variable = RequestContext(request, {'form': form, 'object': nsb })
	return render_to_response(template, variable)

@login_required
def add(request):
    if request.method == 'POST':
        form = NasabahForm(request.POST)

        if form.is_valid():
            nama = form.cleaned_data['nama']
            tgl_lahir = form.cleaned_data['tgl_lahir']
            tempat = form.cleaned_data['tempat']
            no_ktp = form.cleaned_data['no_ktp']
            alamat_ktp = form.cleaned_data['alamat_ktp']
            rt_ktp= form.cleaned_data['rt_ktp']
            rw_ktp= form.cleaned_data['rw_ktp']
            telepon_ktp = form.cleaned_data['telepon_ktp']
            hp_ktp =form.cleaned_data['hp_ktp']
            kelurahan_ktp = form.cleaned_data['kelurahan_ktp']
            kecamatan_ktp = form.cleaned_data['kecamatan_ktp']

            #'''alamat_domisili = form.cleaned_data['alamat_domisili']
            #rt_domisili =form.cleaned_data['rt_domisili']
            #rw_domisili = form.cleaned_data['rw_domisili']
            #telepon_domisili = form.cleaned_data['telepon_domisili']
            #hp_domisili = form.cleaned_data['hp_domisili']
            #kelurahan_domisili = form.cleaned_data['kelurahan_domisili']
            #kecamatan_domisili = form.cleaned_data['kecamatan_domisili']'''
            jenis_pekerjaan = form.cleaned_data['jenis_pekerjaan']
            alamat_kantor = form.cleaned_data['alamat_kantor']
            kode_pos = form.cleaned_data['kode_pos']
            telepon_kantor =form.cleaned_data['telepon_kantor']
            email= form.cleaned_data['email']
            jenis_kelamin= form.cleaned_data['jenis_kelamin']

            nsb= Nasabah (nama = nama, tgl_lahir = tgl_lahir,tempat=tempat, no_ktp =no_ktp,alamat_ktp=alamat_ktp,rt_ktp=rt_ktp,rw_ktp=rw_ktp,telepon_ktp=telepon_ktp,
                hp_ktp=hp_ktp,kelurahan_ktp=kelurahan_ktp,kecamatan_ktp=kecamatan_ktp,
                jenis_pekerjaan=jenis_pekerjaan,alamat_kantor=alamat_kantor,kode_pos=kode_pos,telepon_kantor=telepon_kantor,email=email,jenis_kelamin=jenis_kelamin)
            nsb.save()
            return HttpResponseRedirect('/nasabah/')
    else :
        form = NasabahForm()

    variables = RequestContext(request, {'form': form})
    return render_to_response('nasabah/add.html', variables)

@login_required
def edit(request,object_id):
    n=Nasabah.objects.get(id=object_id)
    template='nasabah/edit.html'
    variable = RequestContext(request,{'n': n})
    return render_to_response(template,variable)


@login_required
def cari(request):
    cari = request.GET['cari']
    pilih = request.GET['pilih']
    if not pilih == '1'  :
        try :
            br = Nasabah.objects.filter(no_ktp__icontains = cari ).order_by('no_ktp')
            if not br   :
                br = Nasabah.objects.filter(no_ktp_istartswith = str(cari)).order_by('nama')
        except :
            pass
    else :
        try :
            br = AkadGadai.objects.filter(no_ktp = cari).order_by("id")[0]
            return HttpResponseRedirect("/nasabah/%s/addnasabah/" % br.id )
        except :
            return  HttpResponseRedirect("/nasabah/add/?no_ktp=%s" % cari )

    if br.count() == 1 :
        return HttpResponseRedirect("/nasabah/%s/show/" % br[0].id)

    template ='nasabah/index.html'
    variable = RequestContext(request,{'object_list': br})
    return render_to_response(template,variable)

### request admin gerai 17-04-2013
@login_required
def cari_nama(request):
    user = request.user
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        nasabah = Nasabah.objects.filter(nama__icontains=q)
        return render_to_response('nasabah/cari_nama.html',
            {'nasabah': nasabah, 'query': q,'user':user})
    else:
        return render_to_response('/', {'error': True})	

