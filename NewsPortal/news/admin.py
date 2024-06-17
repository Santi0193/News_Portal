from django.contrib import admin
from .models import News, Category

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_author', 'created_at')
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('created_at', 'author', 'categories')

    def get_author(self, obj):
        return obj.author.username if obj.author else 'Unknown'
    get_author.short_description = 'Author'
    get_author.admin_order_field = 'author__username'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)