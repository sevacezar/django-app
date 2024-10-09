from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import UserBioForm, UploadFileForm

# Create your views here.

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", '')
    b = request.GET.get("b", '')
    res = a + b
    context = {
        'a': a,
        'b': b,
        'result': res,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)

def user_form(requset: HttpRequest) -> HttpResponse:
    context = {
        'form': UserBioForm(),
    }
    return render(request=requset, template_name='requestdataapp/user-bio-form.html', context=context)

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES['myfile']
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
    else:
        form = UploadFileForm()
    context = {
        # 'message': message,
        'form': form
    }
    return render(request=request, template_name='requestdataapp/file-upload.html', context=context)