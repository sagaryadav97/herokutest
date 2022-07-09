from django.contrib import admin
from .models import *
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display=['id','book_name','book_description','status']
admin.site.register(Book,BookAdmin)

class ReadBookAdmin(admin.ModelAdmin):
    list_display=['id','member','book']
admin.site.register(ReadBook,ReadBookAdmin)