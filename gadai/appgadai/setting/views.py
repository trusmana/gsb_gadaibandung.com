from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from gadai.appgadai.setting.forms import *
from gadai.appgadai.models import Tbl_Cabang,UserProfile

def add_user(request, object_id=None):
    user = None
    if object_id:
        user = User.objects.get(id=int(object_id))
        (up, created) = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        f = UserForm(request.POST)
        if f.is_valid():
            if (f.cleaned_data['gerai']):
                gerai=Tbl_Cabang.objects.get(id=int(f.cleaned_data['gerai']))
            else:
                gerai = None

            rekening = f.cleaned_data['rekening'] or None
            group = f.cleaned_data['group']

            if not user:
                new_user = User.objects.create(
                    username = f.cleaned_data['username'],
                    first_name =  f.cleaned_data['firstname'],
                    last_name = f.cleaned_data['lastname'],
                    email = f.cleaned_data['email'],
                    is_active = True)
                new_user.groups.add(group)

                user_profile = UserProfile.objects.create(
                    user=new_user, 
                    rekening = rekening,
                    gerai = gerai)
                message = "User berhasil dibuat."
            else:
                user.username = f.cleaned_data['username']
                user.first_name = f.cleaned_data['firstname']
                user.last_name = f.cleaned_data['lastname']
                user.email = f.cleaned_data['email']
# hapus group yang nempel pada user
                for g in user.groups.all():
                    user.groups.remove(g)
                user.groups.add(group)
                user.save()

                up.rekening = rekening
                up.gerai = gerai
                up.save()
                message = "User telah diupdate."
            request.user.message_set.create(message=message)
            return HttpResponseRedirect("/setting/user/")
    else:
        if user:
            try:
                gerai = up.gerai.id
            except:
                gerai = None
            f = UserForm(initial={
                'username': user.username,
                'lastname': user.last_name,
                'firstname': user.first_name,
                'email': user.email,
                'rekening': up.rekening,
                'gerai': gerai,
                'group': user.groups.all()[0].id})
        else:
            f = UserForm()
    variables = RequestContext(request, {'form': f, 'user': user})
    return render_to_response('user/add.html', variables)