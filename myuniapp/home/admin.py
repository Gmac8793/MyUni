from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Place)
admin.site.register(Post)
admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(EventMember)