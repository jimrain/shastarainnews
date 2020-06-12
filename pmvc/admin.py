from django.contrib import admin
from .models import Account, Video, GcsAccessToken

admin.site.register(Account)
admin.site.register(Video)
admin.site.register(GcsAccessToken)
