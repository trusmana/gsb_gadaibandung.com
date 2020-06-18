from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gadai.appkeuangan.models import Menu,MenuItem
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from gadai.appgadai.manop.manage.forms import MenuItemForm
from django.template.loader import render_to_string
import json

def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            menu = MenuItem.objects.all()
            data['html_book_list'] = render_to_string('manop/laporan/menu_list.html', {'menu': menu })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, {'form':form,'request':request})
    return json(data)

def menu_update(request, pk):
    menu = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu)
    else:
        form = MenuItemForm(instance=menu)
    return save_book_form(request, form, 'manop/laporan/menu_update.html')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='MANOP'))
def menu_item(request):
    menu = MenuItem.objects.filter(menu__status_aktif__isnull= False)
    list = []
    for a in menu:
        list.append({'akses_group':a.menu.akses_menu,'id':a.id,'judul':a.judul,'nama':a.menu.nama,'pengguna':a.user})
    return render(request, 'manop/laporan/menu_item.html', {'orders': list})
