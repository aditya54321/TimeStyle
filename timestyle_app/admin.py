from django.contrib import admin
from . models import *

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display= ('first_name','is_active')

@admin.register(WatchDesign)
class WatchDesignAdmin(admin.ModelAdmin):
    list_display= ['name']

@admin.register(DesignDetails)
class DesigndetailsAdmin(admin.ModelAdmin):
    list_display = ['watch_design','strap','dial','price']

@admin.register(Order)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display=['user','design','status','quantity']