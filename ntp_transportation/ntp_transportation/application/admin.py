from django.contrib import admin

# Register your models here.

from .models import User, Parcel, Train

admin.site.register(User)
admin.site.register(Parcel)
admin.site.register(Train)
