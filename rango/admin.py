from django.contrib import admin
from rango.models import Category, Page, UserProfile

# Customize Page display
class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url')  # test expects this exact order

# Register Page with PageAdmin
admin.site.register(Page, PageAdmin)

# Register UserProfile separately
admin.site.register(UserProfile)

# Customize Category display
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Register Category with CategoryAdmin
admin.site.register(Category, CategoryAdmin)
