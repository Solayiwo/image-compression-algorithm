from django.contrib import admin # type: ignore
from .models import CustomUser, GuestUser, CompressionTask

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(GuestUser)
admin.site.register(CompressionTask)