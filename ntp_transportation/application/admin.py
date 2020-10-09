from django.contrib import admin

# Register your models here.

from .models import User, Destination, Parcel, Train

admin.site.register(User)
admin.site.register(Destination)
admin.site.register(Parcel)
admin.site.register(Train)
