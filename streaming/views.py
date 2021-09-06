import os
import re
from wsgiref.util import FileWrapper

from streaming.models import Video
from django.shortcuts import render
from djangoTestProject import settings

# Create your views here.
from django.http import StreamingHttpResponse


def index(request):
    print(f'{request.GET=}')
    videos = Video.objects.all()
    return render(request, "streaming/index.html", {'video': videos})


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


def test_stream(request):
    video_path = os.path.join(settings.MEDIA_URL, "video_1.mp4")
    context = {'video_path': video_path}
    return render(request, template_name='streaming/index.html', context=context)


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
