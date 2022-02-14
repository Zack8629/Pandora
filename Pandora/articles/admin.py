from django.contrib import admin

from .models import Category, Articles


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class ArticlesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'content', 'created_at', 'updated_at', 'image', 'published', 'category'
    )
    list_display_links = ('title',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Articles, ArticlesAdmin)
