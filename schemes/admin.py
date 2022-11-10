from django.contrib import admin
from .models import *
# Register your models here.
class SchemesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Schemes, SchemesAdmin)
admin.site.register(Tags)
admin.site.register(Category)
admin.site.register(SubCategory)