from django.shortcuts import render,redirect,render_to_response,RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gadai.appkeuangan.models import Menu,MenuItem
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from gadai.appgadai.manop.manage.forms import MenuItemForm
from django.template.loader import render_to_string
from gadai.appgadai.models import AkadGadai,Nasabah,Barang,ManopPelunasan,ManopPelunasanGu
import datetime


#@login_required
#def data_barang(request):


