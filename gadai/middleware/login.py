###
# Copyright (c) 2006-2007, Jared Kuolt
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the SuperJared.com nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
###
from django.core.context_processors import csrf
from django.conf import settings
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib import auth
from datetime import datetime, timedelta
from gadai.appgadai.models import Visitor
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages

class RequireLoginMiddleware(object):
    def __init__(self):
        self.require_login_path = getattr(settings, 'REQUIRE_LOGIN_PATH', '/accounts/login/')
    def process_request(self, request):
        if request.path.startswith(settings.MEDIA_URL):
            return None
        if request.path != self.require_login_path and request.user.is_anonymous():
            if request.POST:
                return login(request)
            else:
                return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))

class AutoLogout:
  def process_request(self, request):
    if not request.user.is_authenticated() :
      return
    try:
      if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 30, 0):
        auth.logout(request)
        del request.session['last_touch']
        return
    except KeyError:
      pass
    request.session['last_touch'] = datetime.now()

def is_authenticated(user):
    return user.is_authenticated()

class BlokingLogin(object):
    def process_request(self, request):
        if is_authenticated(request.user):
            key_from_cookie = request.session.session_key
            if hasattr(request.user, 'visitor'):
                session_key_in_visitor_db = request.user.visitor.session_key
                if session_key_in_visitor_db != key_from_cookie:
                    SessionStore(session_key_in_visitor_db).delete()
                    request.user.visitor.session_key = key_from_cookie
                    request.user.visitor.save()
                    messages.add_message(request, messages.INFO,'Dilarang Keras Menggunakan User Orang lain')
            else:
                Visitor.objects.create(user=request.user,session_key=key_from_cookie)
