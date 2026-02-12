from django.contrib import admin
from rango.models import Category, Page

# Customize Page display
class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url')  # test expects this exact order

# Register Page with PageAdmin
admin.site.register(Page, PageAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
# Update the registration to include this customised interface
admin.site.register(Category, CategoryAdmin)
