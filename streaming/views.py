import mimetypes
import os
import re
from wsgiref.util import FileWrapper
import cgi

from django.shortcuts import render
from djangoTestProject import settings

# Create your views here.
from django.http import HttpResponse, StreamingHttpResponse


def helping_page(request):
    print(f'{request.POST=}')
    return render(request, 'streaming/registration.html')


def helping_page_post(request):
    print(f'{request.POST=}')


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


def test_stream(request):
    video_path = "media/SampleVideo_1280x720_30mb.mp4"
    context = {'video_path': os.path.join(settings.MEDIA_URL, "SampleVideo_1280x720_30mb.mp4")}
    return render(request, template_name='streaming/index.html', context=context)


def stream_video(request):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    path = os.path.dirname(os.path.abspath(__file__))+"/../SampleVideo_1280x720_30mb.mp4"
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp