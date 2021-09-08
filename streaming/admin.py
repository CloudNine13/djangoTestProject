from django.contrib import admin
from streaming.models import ServiceUser, Video

# Register your models here.
admin.site.register(Video)
admin.site.register(ServiceUser)