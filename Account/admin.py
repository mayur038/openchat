from django.contrib import admin
from .models import *
# Register your models here.
class cuser_display(admin.ModelAdmin):
    list_display = ["username","email","phone","verified","user_profile"]    
admin.site.register(cuser,cuser_display)
admin.site.register(Box)
admin.site.register(Messages)
