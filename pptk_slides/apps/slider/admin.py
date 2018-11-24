from django.contrib import admin

from .models import Slide, SlidePacket


class SlideAdmin(admin.ModelAdmin):
    pass


class SlidePacketAdmin(admin.ModelAdmin):
    pass


admin.site.register(Slide, SlideAdmin)
admin.site.register(SlidePacket, SlidePacketAdmin)
