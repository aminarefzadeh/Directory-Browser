from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

from django.template.loader import get_template
from django.http import HttpResponse

def view_cam(request,cam_id):

    if request.method == 'GET':
        template = get_template('camera/camera.html')
        return HttpResponse(template.render(dict(cam_id=cam_id), request))


def cam_data(request,cam_id):
    pass


def camera_list(request):
    if request.method == 'GET':
        template = get_template('camera/home.html')
        return HttpResponse(template.render(dict(camera_list=[1,3,5,2,6]), request))




from django.urls import path,include
urlpatterns = [
    path('cam/<int:cam_id>/',view_cam),
    path('cam_data/<int:cam_id>/',cam_data),
    path('',camera_list),
]