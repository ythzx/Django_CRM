from django.contrib import admin
from Django_admin import models

admin.site.register(models.UserInfo)
admin.site.register(models.UserGroup)
admin.site.register(models.Role)

