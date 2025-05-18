from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'slug', 'created_at'] # какие поля из таблицы отображать
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ['pk', 'name'] # сделать кликабельными поля указанные в list_display
    list_filter = ['created_at'] # делает панель для фильрации
    search_fields = ['name'] # панель для поиска

admin.site.register(models.Slider)

@admin.register(models.FAQ)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['pk', 'question']
    list_display_links = ['pk', 'question']
    search_fields = ['question']


class ArticleImageInline(admin.TabularInline): # позволяет внедрить один класс в другой
    model = models.ArticleImage
    extra = 1

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views']
    inlines = [ArticleImageInline]

admin.site.register(models.Comment)