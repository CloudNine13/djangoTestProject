import os
import re
from wsgiref.util import FileWrapper

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from djstripe.models import Product

from streaming.forms import SignUpForm
from streaming.models import Video

login_url = '/accounts/login/'


@login_required(login_url=login_url)
def index(request):
    videos = Video.objects.all()
    return render(request, "streaming/index.html", {'video': videos})


@login_required(login_url=login_url)
def checkout(request):
    products = Product.objects.all()
    return render(request, "subscription/checkout.html", {'products': products})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('name')
            password = make_password(form.cleaned_data.get('password'))
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=password, email=email, subscription='Unsubscribed')
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, file_like, blk_size=8192, offset=0, length=None):
        self.file_like = file_like
        self.file_like.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blk_size = blk_size

    def close(self):
        if hasattr(self.file_like, 'close'):
            self.file_like.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.file_like.read(self.blk_size)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.file_like.read(min(self.remaining, self.blk_size))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


@login_required(login_url=login_url)
def stream_video(request, filename):
    video = Video.objects.get(FileName=filename)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    path = video.FileUrl
    size = os.path.getsize(path)
    content_type = 'video/mp4'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp


def landing(request):
    return render(request, template_name='streaming/landing.html')
