from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from gadai.appgadai.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from gadai.appgadai.mankeu.forms import *
from django.contrib import messages
from gadai.appgadai.jurnal.forms import *
###new

def index(request): 
    jurnal_list = Tbl_Transaksi.objects.all()
    trans=[]
    form = Tbl_AkunForm()
    start_date = None
    end_date = None
    id_cabang = None
    if 'id_cabang' in request.GET and request.GET['id_cabang']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        ledger_search = Tbl_Transaksi.objects.filter(id_cabang=id_cabang).filter(tgl_trans__range=(start_date,end_date))   
        trans = []
        for l in ledger_search:           
            trans.append(l)
        start_date = start_date
        id_cabang = id_cabang
        end_date = end_date
    variables = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),'total_kredit': sum([p.kredit for p in trans]),
                'start_date':start_date,'id_cabang':id_cabang,'end_date':start_date})
    return render_to_response('mankeu/index.html', variables)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='MANKEU'))        
def laba_rugi_month(request):
    form = LabaRugiMonthForm()
    #lb_akun = Tbl_Akun.objects.filter(jenis="l").filter(view_unit__in=('0','300'))
    lb_akun = Tbl_Akun.objects.filter(view_unit__in=('300','0')).filter(jenis = "l")
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    month = None
    year = None
    id_cabang = None
    akun =[]
    if  'id_cabang' in request.GET and request.GET['id_cabang']:
        month = request.GET['Bulan_Tahun_month']
        year = request.GET['Bulan_Tahun_year']
        id_cabang = request.GET['id_cabang']
        for c in lb_akun :
            akun.append({'c':c,'deskripsi':c.deskripsi,'debet':c.my_debet_month(id_cabang, month, year),'kredit':c.my_kredit_month(id_cabang, month, year),
                'coa':c.coa,'id':c.id,'kplcoa':300 + (int(id_cabang)),'header_parent':c.header_parent,'tes_coa':int(c.tes_coa()),'saldo':c.saldo_pjb,
                'saldo_akhir':c.saldo_pjb + (int(c.my_debet_month(id_cabang, month, year)) - (int(c.my_kredit_month(id_cabang, month, year))) )})
            month = month
            id_cabang = id_cabang
            year = year    
    template='mankeu/labarugi_month.html'
    variable = RequestContext(request,{'akun':akun, 'form':form,'month':month,'year':year,'id_cabang':id_cabang})
    return render_to_response(template,variable)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='MANKEU'))        
def neraca_pjb_month(request):
    form = LabaRugiMonthForm()
    lb_akun = Tbl_Akun.objects.filter(view_unit__in =('0','300')).filter(jenis__in = 'A,P').order_by('coa')
    akun =[]
    month = None
    year = None
    id_cabang = None
    if  'id_cabang' in request.GET and request.GET['id_cabang']:
        month = request.GET['Bulan_Tahun_month']
        year = request.GET['Bulan_Tahun_year']
        id_cabang = request.GET['id_cabang']
        for c in lb_akun :        
            akun.append({'c':c,'deskripsi':c.deskripsi,'id':c.id,'header_parent':c.header_parent,'debet':(int(c.my_debet_month(id_cabang, month, year))),
                'saldo_akhir':c.saldo_pjb + (int(c.my_debet_month(id_cabang, month, year))) - (int(c.my_kredit_month(id_cabang, month, year))),
                'tes_coa':int(c.tes_coa()),'kode_guna':int(c.kode_guna) })
            month = month
            id_cabang = id_cabang
            year = year
            total_debet = 0
    template='mankeu/neraca_pjb_month.html'
    variable = RequestContext(request,{'akun':akun,'coba':akun, 'form':form, 'id_cabang': id_cabang,'month':month,'year':year,'total_debet':total_debet})
    return render_to_response(template,variable)

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['NONKAS','STAFKEUANGAN'])
#@login_required
#@user_passes_test(is_in_multiple_groups)
def rekapitulasi_transaksi_gl_gl(request):
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(jenis__in=('GL_GL_PUSAT','GL_GL_RAK_PUSAT','GL_GL_RAK_CABANG',
        'Penerimaan Materai','PEMBELIAN MATERAI PUSAT','GL_GL_PENGEMBALIAN_UK','GL_GL_PENGEMBALIAN_UK','Transaksi_Gerai_oleh_Pusat')) 
    template = 'mankeu/stafkeu/rekapitulasi_transaksi_gl_gl.html'
    variables = RequestContext(request, {'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr]),'user':User})
    return render_to_response(template, variables)

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['NONKAS','STAFKEUANGAN'])
#@login_required
#@user_passes_test(is_in_multiple_groups)
def rekapitulasi_transaksi_gl_gl_nonkas(request):
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(jenis='GL_GL_NON_KAS')  
    template = 'mankeu/stafkeu/rekapitulasi_transaksi_gl_gl_non_kas.html'
    variables = RequestContext(request, {'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr]),'user':User})
    return render_to_response(template, variables)
###

##### VIEW APPROVE GL MANOP
@login_required
@user_passes_test(lambda u: u.groups.filter(name='MANKEU'))
def list(request):
    mankeu = Tbl_Transaksi.objects.filter(status_jurnal=1)
    akun=[]
    form = Tbl_AkunForm()
    start_date = None
    end_date = None
    id_cabang = None
    
    if 'start_date' in request.GET and request.GET['start_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        mankeu = Tbl_Transaksi.objects.filter(id_cabang=id_cabang).filter(tgl_trans__range=(start_date,end_date))        
        for c in mankeu :
            akun.append(c)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date
    template = 'mankeu/mankeu.html'
    variables = RequestContext(request, {'mankeu': akun,'form':form,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,
    'total_debet': sum([p.debet for p in akun]),'total_kredit': sum([p.kredit for p in akun]),})    
    return render_to_response(template, variables)

def approve_mankeu_all(request):
    for i in request.POST.getlist('id_pilih'):
        gl = Tbl_Transaksi.objects.get(id=int(i))
        gl.status_jurnal = 2
        messages.add_message(request, messages.INFO,' Input GL manual Terposting.')
        gl.save()
        man = ManopKeu(manop = gl,mankeu=None,status = u'1',tanggal=datetime.date.today())
        man.save()
    return HttpResponseRedirect("/mankeu/")

@login_required
@user_passes_test(lambda u: u.groups.filter(name='MANKEU'))
def approve_mankeu(request, object_id):
    tbl = Tbl_Transaksi.objects.get(id=object_id)
    form = Approve_MankeuForm(initial={'manop': tbl.id})
    form.fields['manop'].widget = forms.HiddenInput()
    form.fields['mankeu'].widget = forms.HiddenInput()
    template = 'mankeu/approve_mankeu.html'
    variable = RequestContext(request, {'tbl': tbl,'form': form})
    return render_to_response(template,variable) 

##### VIEW APPROVE GL MANOP



@login_required
@user_passes_test(lambda u: u.groups.filter(name='mankeu'))
def verifikasi_mankeu(request, object_id):
    tbl = Tbl_Transaksi.objects.get(id=object_id)
    if request.method == 'POST':
        form = Approve_MankeuForm(request.POST)
        if form.is_valid():
            form.save()                
            messages.add_message(request, messages.INFO,'### PROSES APPROVE GL TO GL SUKSES ###')
            if tbl.manopkeu.status == u'2':
                tbl.delete()
            messages.add_message(request, messages.INFO,'### GL TERHAPUS ###')
            return HttpResponseRedirect('/mankeu/')
        else:
            variables = RequestContext(request, {'tbl': tbl, 'form': form})
            return render_to_response('mankeu/approve_mankeu.html', variables)
