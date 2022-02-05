from django.contrib import admin

from .models import Category, Articles


class  CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


class  ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'updated_at', 'image', 'published', 'category')
    list_display_links = ('title',)
    search_fields = ('title', 'content')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Articles, ArticlesAdmin)