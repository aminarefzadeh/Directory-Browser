from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

from django.template.loader import get_template
from django.http import HttpResponse
from app.path import *
from django.http import StreamingHttpResponse,Http404
from app.stream import read_file_chunkwise,stream_data
from django.core.exceptions import PermissionDenied


def check_access(request):
    """Returns true if user has access to the directory"""

    return True

    if request.user.is_anonymous():
        return False
    else:
        return request.user.has_perm('app.readdir_customuser')


def _list_directory(request, directory):
    """default view - listing of the directory"""
    if check_access(request):
        files, directories = get_content(directory)
        directory_name = ('' if (directory == get_abs_root()) else get_rel_path(directory)) + '/'
        data = {
            'directory_name': directory_name,
            'directory_files':[(file,get_rel_path(os.path.join(directory,file)))+streaming_file(os.path.join(directory,file)) for file in files],
            'directory_directories':[(dir,get_rel_path(os.path.join(directory,dir))) for dir in directories],
        }
        template = get_template('dir/directory.html')
        return HttpResponse(template.render(data, request))

    else:
        raise PermissionDenied()



def _show_file(request, file_path):
    """allows authorized user to download a given file"""

    if check_access(request):
        if not streaming_file(file_path)== ('',''):
            content,type = streaming_file(file_path)
            data={
                'content':content,
                'type':type,
                'filename':os.path.basename(file_path),
                'link':get_rel_path(file_path),
            }
            template = get_template('dir/show_file.html')
            return HttpResponse(template.render(data, request))
        else:
            raise Http404
    else:
        raise PermissionDenied()


def browse(request, path):
    if request.method == 'GET':
        virtual_root = get_abs_root()
        eventual_path = get_abs_path(os.path.join(virtual_root, path))

        if not is_inside_root(eventual_path):
            # Someone is playing tricks with .. or %2e%2e or so
            raise Http404

        if os.path.isfile(eventual_path):
            return _show_file(request, eventual_path)
        else:
            return _list_directory(request, eventual_path)


def download_file(request,path):
    if request.method == 'GET':
        virtual_root = get_abs_root()
        eventual_path = get_abs_path(os.path.join(virtual_root, path))
        if not is_inside_root(eventual_path):
            # Someone is playing tricks with .. or %2e%2e or so
            raise Http404

        if os.path.isfile(eventual_path):
            response = StreamingHttpResponse(content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(eventual_path)
            file_obj = open(eventual_path, 'rb')
            response.streaming_content = read_file_chunkwise(file_obj)
            return response

        else:
            raise Http404




def stream_file(request,path):
    if request.method == 'GET':
        virtual_root = get_abs_root()
        eventual_path = get_abs_path(os.path.join(virtual_root, path))
        if not is_inside_root(eventual_path):
            # Someone is playing tricks with .. or %2e%2e or so
            raise Http404

        if os.path.isfile(eventual_path):
            if not streaming_file(eventual_path) == ('',''):
                return stream_data(request,eventual_path,False)

        raise Http404



from django.conf.urls import url

urlpatterns = [
    url(r'^stream/(?P<path>.*)$',stream_file),
    url(r'^download/(?P<path>.*)$',download_file),
    url(r'^browse/(?P<path>.*)$',browse),
]