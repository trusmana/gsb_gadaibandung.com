from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
from django.views.generic import create_update, list_detail
from django.template import RequestContext
from django.contrib.auth.models import User,Group
from django.shortcuts import render_to_response
from django import forms
from gadai.appgadai.models import *
import datetime
from django.utils.html import escape###MENU POP UP
from gadai.appgadai.report.forms import *


def agingharian(request):
    sekarang = datetime.date.today()   
    trans = []    
    form = AgingForm()
    if 'start_date' in request.GET and 'submit' in request.GET:
        start_date = request.GET['start_date']
        cab = Tbl_Cabang.objects.all().order_by('id')
        #barang_a = Tbl_Cabang.objects.filter(akadgadai__tanggal=(tanggal)).order_by('id')
        for t in cab:
            trans.append({'t':t,'nama_cabang':t.nama_cabang,'kode_cabang':t.kode_cabang,'jumlah_aging_hp_filter':t.jumlah_aging_hp_filter(start_date),\
                'total_pinjaman_aging_hp_filter':t.total_pinjaman_aging_hp_filter(start_date),
                'jumlah_aging_laptop_filter':t.jumlah_aging_laptop_filter(start_date),
                'total_pinjaman_aging_laptop_filter':t.total_pinjaman_aging_laptop_filter(start_date),
                'jumlah_aging_kamera_filter':t.jumlah_aging_kamera_filter(start_date),
                'total_pinjaman_aging_kamera_filter':t.total_pinjaman_aging_kamera_filter(start_date),
                'jumlah_aging_ps_filter':t.jumlah_aging_ps_filter(start_date),
                'total_pinjaman_aging_ps_filter':t.total_pinjaman_aging_ps_filter(start_date),
                'jumlah_aging_tv_filter':t.jumlah_aging_tv_filter(start_date),
                'total_pinjaman_aging_tv_filter':t.total_pinjaman_aging_tv_filter(start_date),
                'jumlah_aging_motor_filter':t.jumlah_aging_motor_filter(start_date),
                'total_pinjaman_aging_motor_filter':t.total_pinjaman_aging_motor_filter(start_date),
                'jumlah_aging_mobil_filter':t.jumlah_aging_mobil_filter(start_date),
                'total_pinjaman_aging_mobil_filter':t.total_pinjaman_aging_mobil_filter(start_date),
                'total_aging_hari_filter':t.total_aging_hari_filter(start_date),####batas pencairan
                'lelang_aging_hp_filter':t.lelang_aging_hp_filter(start_date),
                'total_lelang_aging_hp_filter':t.total_lelang_aging_hp_filter(start_date),
                'lelang_aging_laptop_filter':t.lelang_aging_laptop_filter(start_date),
                'total_lelang_aging_laptop_filter':t.total_lelang_aging_laptop_filter(start_date),
                'lelang_aging_kamera_filter':t.lelang_aging_kamera_filter(start_date),
                'total_lelang_aging_kamera_filter':t.total_lelang_aging_kamera_filter(start_date),
                'lelang_aging_ps_filter':t.lelang_aging_ps_filter(start_date),
                'total_lelang_aging_ps_filter':t.total_lelang_aging_ps_filter(start_date),
                'lelang_aging_tv_filter':t.lelang_aging_tv_filter(start_date),
                'total_lelang_aging_tv_filter':t.total_lelang_aging_tv_filter(start_date),
                'lelang_aging_motor_filter':t.lelang_aging_motor_filter(start_date),
                'total_lelang_aging_motor_filter':t.total_lelang_aging_motor_filter(start_date),
                'lelang_aging_mobil_filter':t.lelang_aging_mobil_filter(start_date),
                'total_lelang_aging_mobil_filter':t.total_lelang_aging_mobil_filter(start_date),
                'total_lelangaging_hari_filter':t.total_lelangaging_hari_filter(start_date),###batas lelang
                'pelunasan_aging_hp_filter':t.pelunasan_aging_hp_filter(start_date),
                'total_pelunasan_aging_hp_filter':t.total_pelunasan_aging_hp_filter(start_date),
                'pelunasan_aging_laptop_filter':t.pelunasan_aging_laptop_filter(start_date),
                'total_pelunasan_aging_laptop_filter':t.total_pelunasan_aging_laptop_filter(start_date),
                'pelunasan_aging_kamera_filter':t.pelunasan_aging_kamera_filter(start_date),
                'total_pelunasan_aging_kamera_filter':t.total_pelunasan_aging_kamera_filter(start_date),
                'pelunasan_aging_ps_filter':t.pelunasan_aging_ps_filter(start_date),
                'total_pelunasan_aging_ps_filter':t.total_pelunasan_aging_ps_filter(start_date),
                'pelunasan_aging_tv_filter':t.pelunasan_aging_tv_filter(start_date),
                'total_pelunasan_aging_tv_filter':t.total_pelunasan_aging_tv_filter(start_date),
                'pelunasan_aging_motor_filter':t.pelunasan_aging_motor_filter(start_date),
                'total_pelunasan_aging_motor_filter':t.total_pelunasan_aging_motor_filter(start_date),
                'pelunasan_aging_mobil_filter':t.pelunasan_aging_mobil_filter(start_date),
                'total_pelunasan_aging_mobil_filter':t.total_pelunasan_aging_mobil_filter(start_date),
                'total_lunasaging_hari_filter':t.total_lunasaging_hari_filter(start_date), 

                'retur_aging_hp_filter':t.retur_aging_hp_filter(start_date),
                'total_retur_aging_hp_filter':t.total_retur_aging_hp_filter(start_date),
                'retur_aging_laptop_filter':t.retur_aging_laptop_filter(start_date),    
                'total_retur_aging_laptop_filter':t.total_pelunasan_aging_laptop_filter(start_date),
                'retur_aging_kamera_filter':t.retur_aging_kamera_filter(start_date),
                'total_retur_aging_kamera_filter':t.total_retur_aging_kamera_filter(start_date),
                'retur_aging_ps_filter':t.retur_aging_ps_filter(start_date),
                'total_retur_aging_ps_filter':t.total_retur_aging_ps_filter(start_date),
                'retur_aging_tv_filter':t.retur_aging_tv_filter(start_date),
                'total_retur_aging_tv_filter':t.total_retur_aging_tv_filter(start_date),
                'retur_aging_motor_filter':t.retur_aging_motor_filter(start_date),
                'total_retur_aging_motor_filter':t.total_retur_aging_motor_filter(start_date),
                'retur_aging_mobil_filter':t.retur_aging_mobil_filter(start_date),
                'total_retur_aging_mobil_filter':t.total_retur_aging_mobil_filter(start_date),
                'total_returaging_hari_filter':t.total_returaging_hari_filter(start_date),
                })
        template='report/detailharian_filter.html'
        variable = RequestContext(request,{'form':form,'barang':trans,'start_date':start_date,\
            'tot_jumlah_aging_hp_filter':sum([p.jumlah_aging_hp_filter(start_date) for p in cab]),\
            'tot_total_pinjaman_aging_hp_filter':sum([p.total_pinjaman_aging_hp_filter(start_date) for p in cab]),\
            'tot_jumlah_aging_laptop_filter':sum([p.jumlah_aging_laptop_filter(start_date) for p in cab]),\
            'tot_total_pinjaman_aging_laptop_filter':sum([p.total_pinjaman_aging_laptop_filter(start_date) for p in cab]),
            'tot_jumlah_aging_kamera_filter':sum([p.jumlah_aging_kamera_filter(start_date) for p in cab ]),
            'tot_total_pinjaman_aging_kamera_filter':sum([p.total_pinjaman_aging_kamera_filter(start_date) for p in cab ]),
            'tot_jumlah_aging_ps_filter':sum([p.jumlah_aging_ps_filter(start_date) for p in cab]),
            'tot_total_pinjaman_aging_ps_filter':sum([p.total_pinjaman_aging_ps_filter(start_date) for p in cab]),
            'tot_jumlah_aging_tv_filter':sum([p.jumlah_aging_tv_filter(start_date) for p in cab]),
            'tot_total_pinjaman_aging_tv_filter':sum([p.total_pinjaman_aging_tv_filter(start_date) for p in cab]),
            'tot_jumlah_aging_motor_filter':sum([p.jumlah_aging_motor_filter(start_date) for p in cab]),
            'tot_total_pinjaman_aging_motor_filter':sum([p.total_pinjaman_aging_motor_filter(start_date) for p in cab]),
            'tot_jumlah_aging_mobil_filter':sum([p.jumlah_aging_mobil_filter(start_date) for p in cab ]),
            'tot_total_pinjaman_aging_mobil_filter':sum([p.total_pinjaman_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_aging_hari_filter':sum([p.total_aging_hari_filter(start_date) for p in cab]),

            'tot_lelang_aging_hp_filter':sum([p.lelang_aging_hp_filter(start_date) for p in cab]),
            'tot_total_lelang_aging_hp_filter':sum([p.total_lelang_aging_hp_filter(start_date) for p in cab]),
            'tot_lelang_aging_laptop_filter':sum([p.lelang_aging_laptop_filter(start_date) for p in cab ]),
            'tot_total_lelang_aging_laptop_filter':sum([p.total_lelang_aging_laptop_filter(start_date) for p in cab]),
            'tot_lelang_aging_kamera_filter':sum([p.lelang_aging_kamera_filter(start_date) for p in cab]),
            'tot_total_lelang_aging_kamera_filter':sum([p.total_lelang_aging_kamera_filter(start_date) for p in cab]),
            'tot_lelang_aging_ps_filter':sum([p.lelang_aging_ps_filter(start_date) for p in cab ]),
            'tot_total_lelang_aging_ps_filter':sum([p.total_lelang_aging_ps_filter(start_date) for p in cab]),
            'tot_lelang_aging_tv_filter':sum([p.lelang_aging_tv_filter(start_date) for p in cab]),
            'tot_total_lelang_aging_tv_filter':sum([p.total_lelang_aging_tv_filter(start_date) for p in cab]),
            'tot_lelang_aging_motor_filter':sum([p.lelang_aging_motor_filter(start_date) for p in cab]),
            'tot_total_lelang_aging_motor_filter':sum([p.total_lelang_aging_motor_filter(start_date) for p in cab]),
            'tot_lelang_aging_mobil_filter':sum([p.lelang_aging_mobil_filter(start_date) for p in cab ]),
            'tot_total_lelang_aging_mobil_filter':sum([p.total_lelang_aging_mobil_filter(start_date) for p in cab ]),
            'tot_total_lelangaging_hari_filter':sum([p.total_lelangaging_hari_filter(start_date) for p in cab]),

            'tot_pelunasan_aging_hp_filter':sum([p.pelunasan_aging_hp_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_hp_filter':sum([p.total_pelunasan_aging_hp_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_laptop_filter':sum([p.pelunasan_aging_laptop_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_laptop_filter':sum([p.total_pelunasan_aging_laptop_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_kamera_filter':sum([p.pelunasan_aging_kamera_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_kamera_filter':sum([p.total_pelunasan_aging_kamera_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_ps_filter':sum([p.pelunasan_aging_ps_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_ps_filter':sum([p.total_pelunasan_aging_ps_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_tv_filter':sum([p.pelunasan_aging_tv_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_tv_filter':sum([p.total_pelunasan_aging_tv_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_motor_filter':sum([p.pelunasan_aging_motor_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_motor_filter':sum([p.total_pelunasan_aging_motor_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_mobil_filter':sum([p.pelunasan_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_mobil_filter':sum([p.total_pelunasan_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_lunasaging_hari_filter':sum([p.total_lunasaging_hari_filter(start_date) for p in cab]),

            'tot_retur_aging_hp_filter':sum([p.retur_aging_hp_filter(start_date) for p in cab]),
            'tot_total_retur_aging_hp_filter':sum([p.total_retur_aging_hp_filter(start_date) for p in cab]),
            'tot_retur_aging_laptop_filter':sum([p.retur_aging_laptop_filter(start_date) for p in cab]),    
            'tot_total_retur_aging_laptop_filter':sum([p.total_pelunasan_aging_laptop_filter(start_date) for p in cab]),
            'tot_retur_aging_kamera_filter':sum([p.retur_aging_kamera_filter(start_date) for p in cab]),
            'tot_total_retur_aging_kamera_filter':sum([p.total_retur_aging_kamera_filter(start_date) for p in cab]),
            'tot_retur_aging_ps_filter':sum([p.retur_aging_ps_filter(start_date) for p in cab]),
            'tot_total_retur_aging_ps_filter':sum([p.total_retur_aging_ps_filter(start_date) for p in cab]),
            'tot_retur_aging_tv_filter':sum([p.retur_aging_tv_filter(start_date) for p in cab]),
            'tot_total_retur_aging_tv_filter':sum([p.total_retur_aging_tv_filter(start_date) for p in cab]),
            'tot_retur_aging_motor_filter':sum([p.retur_aging_motor_filter(start_date) for p in cab]),
            'tot_total_retur_aging_motor_filter':sum([p.total_retur_aging_motor_filter(start_date) for p in cab]),
            'tot_retur_aging_mobil_filter':sum([p.retur_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_retur_aging_mobil_filter':sum([p.total_retur_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_returaging_hari_filter':sum([p.total_returaging_hari_filter(start_date) for p in cab]),
            })
        return render_to_response(template,variable)

    if 'start_date' in request.GET and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        cab = Tbl_Cabang.objects.all().order_by('id')
        #barang_a = Tbl_Cabang.objects.filter(akadgadai__tanggal=(tanggal)).order_by('id')
        for t in cab:
            trans.append({'t':t,'nama_cabang':t.nama_cabang,'kode_cabang':t.kode_cabang,'jumlah_aging_hp_filter':t.jumlah_aging_hp_filter(start_date),\
                'total_pinjaman_aging_hp_filter':t.total_pinjaman_aging_hp_filter(start_date),
                'jumlah_aging_laptop_filter':t.jumlah_aging_laptop_filter(start_date),
                'total_pinjaman_aging_laptop_filter':t.total_pinjaman_aging_laptop_filter(start_date),
                'jumlah_aging_kamera_filter':t.jumlah_aging_kamera_filter(start_date),
                'total_pinjaman_aging_kamera_filter':t.total_pinjaman_aging_kamera_filter(start_date),
                'jumlah_aging_ps_filter':t.jumlah_aging_ps_filter(start_date),
                'total_pinjaman_aging_ps_filter':t.total_pinjaman_aging_ps_filter(start_date),
                'jumlah_aging_tv_filter':t.jumlah_aging_tv_filter(start_date),
                'total_pinjaman_aging_tv_filter':t.total_pinjaman_aging_tv_filter(start_date),
                'jumlah_aging_motor_filter':t.jumlah_aging_motor_filter(start_date),
                'total_pinjaman_aging_motor_filter':t.total_pinjaman_aging_motor_filter(start_date),
                'jumlah_aging_mobil_filter':t.jumlah_aging_mobil_filter(start_date),
                'total_pinjaman_aging_mobil_filter':t.total_pinjaman_aging_mobil_filter(start_date),
                'total_aging_hari_filter':t.total_aging_hari_filter(start_date),####batas pencairan
                'lelang_aging_hp_filter':t.lelang_aging_hp_filter(start_date),
                'total_lelang_aging_hp_filter':t.total_lelang_aging_hp_filter(start_date),
                'lelang_aging_laptop_filter':t.lelang_aging_laptop_filter(start_date),
                'total_lelang_aging_laptop_filter':t.total_lelang_aging_laptop_filter(start_date),
                'lelang_aging_kamera_filter':t.lelang_aging_kamera_filter(start_date),
                'total_lelang_aging_kamera_filter':t.total_lelang_aging_kamera_filter(start_date),
                'lelang_aging_ps_filter':t.lelang_aging_ps_filter(start_date),
                'total_lelang_aging_ps_filter':t.total_lelang_aging_ps_filter(start_date),
                'lelang_aging_tv_filter':t.lelang_aging_tv_filter(start_date),
                'total_lelang_aging_tv_filter':t.total_lelang_aging_tv_filter(start_date),
                'lelang_aging_motor_filter':t.lelang_aging_motor_filter(start_date),
                'total_lelang_aging_motor_filter':t.total_lelang_aging_motor_filter(start_date),
                'lelang_aging_mobil_filter':t.lelang_aging_mobil_filter(start_date),
                'total_lelang_aging_mobil_filter':t.total_lelang_aging_mobil_filter(start_date),
                'total_lelangaging_hari_filter':t.total_lelangaging_hari_filter(start_date),###batas lelang
                'pelunasan_aging_hp_filter':t.pelunasan_aging_hp_filter(start_date),
                'total_pelunasan_aging_hp_filter':t.total_pelunasan_aging_hp_filter(start_date),
                'pelunasan_aging_laptop_filter':t.pelunasan_aging_laptop_filter(start_date),
                'total_pelunasan_aging_laptop_filter':t.total_pelunasan_aging_laptop_filter(start_date),
                'pelunasan_aging_kamera_filter':t.pelunasan_aging_kamera_filter(start_date),
                'total_pelunasan_aging_kamera_filter':t.total_pelunasan_aging_kamera_filter(start_date),
                'pelunasan_aging_ps_filter':t.pelunasan_aging_ps_filter(start_date),
                'total_pelunasan_aging_ps_filter':t.total_pelunasan_aging_ps_filter(start_date),
                'pelunasan_aging_tv_filter':t.pelunasan_aging_tv_filter(start_date),
                'total_pelunasan_aging_tv_filter':t.total_pelunasan_aging_tv_filter(start_date),
                'pelunasan_aging_motor_filter':t.pelunasan_aging_motor_filter(start_date),
                'total_pelunasan_aging_motor_filter':t.total_pelunasan_aging_motor_filter(start_date),
                'pelunasan_aging_mobil_filter':t.pelunasan_aging_mobil_filter(start_date),
                'total_pelunasan_aging_mobil_filter':t.total_pelunasan_aging_mobil_filter(start_date),
                'total_lunasaging_hari_filter':t.total_lunasaging_hari_filter(start_date), 

                'retur_aging_hp_filter':t.retur_aging_hp_filter(start_date),
                'total_retur_aging_hp_filter':t.total_retur_aging_hp_filter(start_date),
                'retur_aging_laptop_filter':t.retur_aging_laptop_filter(start_date),    
                'total_retur_aging_laptop_filter':t.total_pelunasan_aging_laptop_filter(start_date),
                'retur_aging_kamera_filter':t.retur_aging_kamera_filter(start_date),
                'total_retur_aging_kamera_filter':t.total_retur_aging_kamera_filter(start_date),
                'retur_aging_ps_filter':t.retur_aging_ps_filter(start_date),
                'total_retur_aging_ps_filter':t.total_retur_aging_ps_filter(start_date),
                'retur_aging_tv_filter':t.retur_aging_tv_filter(start_date),
                'total_retur_aging_tv_filter':t.total_retur_aging_tv_filter(start_date),
                'retur_aging_motor_filter':t.retur_aging_motor_filter(start_date),
                'total_retur_aging_motor_filter':t.total_retur_aging_motor_filter(start_date),
                'retur_aging_mobil_filter':t.retur_aging_mobil_filter(start_date),
                'total_retur_aging_mobil_filter':t.total_retur_aging_mobil_filter(start_date),
                'total_returaging_hari_filter':t.total_returaging_hari_filter(start_date),
                })
        template='report/cetakdetailhari.html'
        variable = RequestContext(request,{'form':form,'barang':trans,'start_date':start_date,\
            'tot_jumlah_aging_hp_filter':sum([p.jumlah_aging_hp_filter(start_date) for p in cab]),\
            'tot_total_pinjaman_aging_hp_filter':sum([p.total_pinjaman_aging_hp_filter(start_date) for p in cab]),\
            'tot_jumlah_aging_laptop_filter':sum([p.jumlah_aging_laptop_filter(start_date) for p in cab]),\
            'tot_total_pinjaman_aging_laptop_filter':sum([p.total_pinjaman_aging_laptop_filter(start_date) for p in cab]),
            'tot_jumlah_aging_kamera_filter':sum([p.jumlah_aging_kamera_filter(start_date) for p in cab ]),
            'tot_total_pinjaman_aging_kamera_filter':sum([p.total_pinjaman_aging_kamera_filter(start_date) for p in cab ]),
            'tot_jumlah_aging_ps_filter':sum([p.jumlah_aging_ps_filter(start_date) for p in cab]),
            'tot_total_pinjaman_aging_ps_filter':sum([p.total_pinjaman_aging_ps_filter(start_date) for p in cab]),
            'tot_jumlah_aging_tv_filter':sum([p.jumlah_aging_tv_filter(start_date) for p in cab]),
            'tot_total_pinjaman_aging_tv_filter':sum([p.total_pinjaman_aging_tv_filter(start_date) for p in cab]),
            'tot_jumlah_aging_motor_filter':sum([p.jumlah_aging_motor_filter(start_date) for p in cab]),
            'tot_total_pinjaman_aging_motor_filter':sum([p.total_pinjaman_aging_motor_filter(start_date) for p in cab]),
            'tot_jumlah_aging_mobil_filter':sum([p.jumlah_aging_mobil_filter(start_date) for p in cab ]),
            'tot_total_pinjaman_aging_mobil_filter':sum([p.total_pinjaman_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_aging_hari_filter':sum([p.total_aging_hari_filter(start_date) for p in cab]),

            'tot_lelang_aging_hp_filter':sum([p.lelang_aging_hp_filter(start_date) for p in cab]),
            'tot_total_lelang_aging_hp_filter':sum([p.total_lelang_aging_hp_filter(start_date) for p in cab]),
            'tot_lelang_aging_laptop_filter':sum([p.lelang_aging_laptop_filter(start_date) for p in cab ]),
            'tot_total_lelang_aging_laptop_filter':sum([p.total_lelang_aging_laptop_filter(start_date) for p in cab]),
            'tot_lelang_aging_kamera_filter':sum([p.lelang_aging_kamera_filter(start_date) for p in cab]),
            'tot_total_lelang_aging_kamera_filter':sum([p.total_lelang_aging_kamera_filter(start_date) for p in cab]),
            'tot_lelang_aging_ps_filter':sum([p.lelang_aging_ps_filter(start_date) for p in cab ]),
            'tot_total_lelang_aging_ps_filter':sum([p.total_lelang_aging_ps_filter(start_date) for p in cab]),
            'tot_lelang_aging_tv_filter':sum([p.lelang_aging_tv_filter(start_date) for p in cab]),
            'tot_total_lelang_aging_tv_filter':sum([p.total_lelang_aging_tv_filter(start_date) for p in cab]),
            'tot_lelang_aging_motor_filter':sum([p.lelang_aging_motor_filter(start_date) for p in cab]),
            'tot_total_lelang_aging_motor_filter':sum([p.total_lelang_aging_motor_filter(start_date) for p in cab]),
            'tot_lelang_aging_mobil_filter':sum([p.lelang_aging_mobil_filter(start_date) for p in cab ]),
            'tot_total_lelang_aging_mobil_filter':sum([p.total_lelang_aging_mobil_filter(start_date) for p in cab ]),
            'tot_total_lelangaging_hari_filter':sum([p.total_lelangaging_hari_filter(start_date) for p in cab]),

            'tot_pelunasan_aging_hp_filter':sum([p.pelunasan_aging_hp_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_hp_filter':sum([p.total_pelunasan_aging_hp_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_laptop_filter':sum([p.pelunasan_aging_laptop_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_laptop_filter':sum([p.total_pelunasan_aging_laptop_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_kamera_filter':sum([p.pelunasan_aging_kamera_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_kamera_filter':sum([p.total_pelunasan_aging_kamera_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_ps_filter':sum([p.pelunasan_aging_ps_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_ps_filter':sum([p.total_pelunasan_aging_ps_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_tv_filter':sum([p.pelunasan_aging_tv_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_tv_filter':sum([p.total_pelunasan_aging_tv_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_motor_filter':sum([p.pelunasan_aging_motor_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_motor_filter':sum([p.total_pelunasan_aging_motor_filter(start_date) for p in cab]),
            'tot_pelunasan_aging_mobil_filter':sum([p.pelunasan_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_pelunasan_aging_mobil_filter':sum([p.total_pelunasan_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_lunasaging_hari_filter':sum([p.total_lunasaging_hari_filter(start_date) for p in cab]),

            'tot_retur_aging_hp_filter':sum([p.retur_aging_hp_filter(start_date) for p in cab]),
            'tot_total_retur_aging_hp_filter':sum([p.total_retur_aging_hp_filter(start_date) for p in cab]),
            'tot_retur_aging_laptop_filter':sum([p.retur_aging_laptop_filter(start_date) for p in cab]),    
            'tot_total_retur_aging_laptop_filter':sum([p.total_pelunasan_aging_laptop_filter(start_date) for p in cab]),
            'tot_retur_aging_kamera_filter':sum([p.retur_aging_kamera_filter(start_date) for p in cab]),
            'tot_total_retur_aging_kamera_filter':sum([p.total_retur_aging_kamera_filter(start_date) for p in cab]),
            'tot_retur_aging_ps_filter':sum([p.retur_aging_ps_filter(start_date) for p in cab]),
            'tot_total_retur_aging_ps_filter':sum([p.total_retur_aging_ps_filter(start_date) for p in cab]),
            'tot_retur_aging_tv_filter':sum([p.retur_aging_tv_filter(start_date) for p in cab]),
            'tot_total_retur_aging_tv_filter':sum([p.total_retur_aging_tv_filter(start_date) for p in cab]),
            'tot_retur_aging_motor_filter':sum([p.retur_aging_motor_filter(start_date) for p in cab]),
            'tot_total_retur_aging_motor_filter':sum([p.total_retur_aging_motor_filter(start_date) for p in cab]),
            'tot_retur_aging_mobil_filter':sum([p.retur_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_retur_aging_mobil_filter':sum([p.total_retur_aging_mobil_filter(start_date) for p in cab]),
            'tot_total_returaging_hari_filter':sum([p.total_returaging_hari_filter(start_date) for p in cab]),
            })
        return render_to_response(template,variable)
    else:
        template='report/detailharian_filter.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)


def tampil(request, object_id):
    gg = Tbl_Cabang.objects.get(id=object_id)
    pk=AkadGadai.objects.all()
    try:
        barang=int(request.POST['barang'])
    except:
        barang=1
    sekarang = datetime.datetime.now()
    barang = dict(JENIS_BARANG)
    p  = pk.filter(gerai=gg).filter(barang__jenis_barang=1).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    d  = pk.filter(gerai=gg).filter(barang__jenis_barang=1).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    p1 = pk.filter(gerai=gg).filter(barang__jenis_barang=2).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    d1 = pk.filter(gerai=gg).filter(barang__jenis_barang=2).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    p2 = pk.filter(gerai=gg).filter(barang__jenis_barang=3).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    d2 = pk.filter(gerai=gg).filter(barang__jenis_barang=3).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    p3 = pk.filter(gerai=gg).filter(barang__jenis_barang=4).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    d3 = pk.filter(gerai=gg).filter(barang__jenis_barang=4).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)    
    p4 = pk.filter(gerai=gg).filter(barang__jenis_barang=5).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    d4 = pk.filter(gerai=gg).filter(barang__jenis_barang=5).filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)

    c   = pk.filter(gerai=gg).filter(barang__jenis_barang=1).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    e   = pk.filter(gerai=gg).filter(barang__jenis_barang=1).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    c1  = pk.filter(gerai=gg).filter(barang__jenis_barang=2).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    e1  = pk.filter(gerai=gg).filter(barang__jenis_barang=2).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    c2  = pk.filter(gerai=gg).filter(barang__jenis_barang=3).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    e2  = pk.filter(gerai=gg).filter(barang__jenis_barang=3).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    c3  = pk.filter(gerai=gg).filter(barang__jenis_barang=4).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    e3  = pk.filter(gerai=gg).filter(barang__jenis_barang=4).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)        
    c4  = pk.filter(gerai=gg).filter(barang__jenis_barang=5).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    e4  = pk.filter(gerai=gg).filter(barang__jenis_barang=5).filter(status_transaksi='LELANG').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)

    aa   = pk.filter(gerai=gg).filter(barang__jenis_barang=1).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    bb   = pk.filter(gerai=gg).filter(barang__jenis_barang=1).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    aa1  = pk.filter(gerai=gg).filter(barang__jenis_barang=2).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    bb1  = pk.filter(gerai=gg).filter(barang__jenis_barang=2).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    aa2  = pk.filter(gerai=gg).filter(barang__jenis_barang=3).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    bb2  = pk.filter(gerai=gg).filter(barang__jenis_barang=3).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    aa3  = pk.filter(gerai=gg).filter(barang__jenis_barang=4).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    bb3  = pk.filter(gerai=gg).filter(barang__jenis_barang=4).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)        
    aa4  = pk.filter(gerai=gg).filter(barang__jenis_barang=5).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year).count()
    bb4  = pk.filter(gerai=gg).filter(barang__jenis_barang=5).filter(lunas__isnull='True').filter(tanggal__month=sekarang.month).filter(tanggal__year=sekarang.year)
    variables = RequestContext(request, {'object': gg,
    'nilai': sum([b.nilai for b in d]),'nilai1': sum([b.nilai for b in d1]),'nilai2': sum([b.nilai for b in d2]),
    'nilai3': sum([b.nilai for b in d3]),'nilai4': sum([b.nilai for b in d4]), 
    'total': sum([b.nilai for b in d]) + sum([b.nilai for b in d1]) + sum([b.nilai for b in d2]) + sum([b.nilai for b in d3]) + sum([b.nilai for b in d4]),
    'nilailelang': sum([b.nilai for b in e]),'nilailelang1': sum([b.nilai for b in e1]),'nilailelang2': sum([b.nilai for b in e2]),
    'nilailelang3': sum([b.nilai for b in e3]),'nilailelang4': sum([b.nilai for b in e4]),
    'totallelang': sum([b.nilai for b in e]) + sum([b.nilai for b in e1]) + sum([b.nilai for b in e2]) + sum([b.nilai for b in e3]) + sum([b.nilai for b in e4]),
    'p': p,'p1': p1,'p2': p2,'p3': p3,'p4': p4,'kelompok': JENIS_BARANG,'np': p,
    'c':c,'c1':c1,'c2':c2,'c3':c3,'c4':c4,'e':e,'e1':e1,'e2':e2,'e3':e3,'e4':e4,'aa':aa,'aa1':aa1,'aa2':aa2,'aa3':aa3,'aa4':aa4,'bb':bb,'bb1':bb1,'bb2':bb2,'bb3':bb3,'bb4':bb4,
    'nilailunas': sum([b.nilai for b in bb]),'nilailunas1': sum([b.nilai for b in bb1]),'nilailunas2': sum([b.nilai for b in bb2]),
    'nilailunas3': sum([b.nilai for b in bb3]),'nilailunas4': sum([b.nilai for b in bb4]),
    'totallunas': sum([b.nilai for b in bb]) + sum([b.nilai for b in bb1]) + sum([b.nilai for b in bb2]) + sum([b.nilai for b in bb3]) + sum([b.nilai for b in bb4]),})
    return render_to_response('report/detail.html', variables)

