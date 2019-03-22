from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

from django.template.loader import get_template
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        uf = UserCreationForm(request.POST, prefix='user')
        if uf.is_valid() :
            user = uf.save()
            return HttpResponseRedirect("/")
    else:
        template = get_template('registration/register.html')
        uf = UserCreationForm(prefix='user')
        return HttpResponse(template.render(dict(userform=uf),request))



# you can eather use UserCreationForm in default auth forms or you can create custome form like in forms.UserForm but
# remember that you should get_clean_data("password") and setPassword for user because of hash