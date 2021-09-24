from django.contrib import admin
from streaming.models import ServiceUser, Video


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


# Register your models here.
admin.site.register(Video)
admin.site.register(ServiceUser, UserAdmin)
