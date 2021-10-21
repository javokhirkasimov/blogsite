from django.contrib import admin

from .models import Category,Blog, Hashtags, PicturesFromTheBlog, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'category', 'image_tag')
    readonly_fields = ('image_tag',)



@admin.register(Hashtags)
class HashtagsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(PicturesFromTheBlog)
class PicturesAdmin(admin.ModelAdmin):
    list_display = ('owner',)



