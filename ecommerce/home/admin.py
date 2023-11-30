from django.contrib import admin
from .import views
from .models import *
# Register your models here.

class catadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(categ,catadmin)

class prodadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(product,prodadmin)