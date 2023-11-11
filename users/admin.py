from django.contrib import admin
from .models import *


# Register your models here.
#

class RoomAdmin(admin.ModelAdmin):
    """ Representation of the story telling room in admin panel """
    list_display = ('topic', 'name', 'description')


class MessageAdmin(admin.ModelAdmin):
    """ Representation of the comments int the form messages in admin panel """
    list_display = ('room', 'updated', 'created')


admin.site.register(Room, RoomAdmin)
admin.site.register(Topic)
admin.site.register(Message, MessageAdmin)
admin.site.register(User)
