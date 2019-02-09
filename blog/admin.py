from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Post, PostImage, Tag


class ImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    fieldsets = [
        ('Post Images',     {'fields': ['image_title', 'image']})
    ]


class PostAdmin(admin.ModelAdmin):
    # used for organizing the admin editing interface
    fieldsets = [
        (None, {'fields': [
            'title', 'author', 'slug', 'tags', 'post']}),
        ('Date information', {'fields': ['pub_date', ]}),
    ]
    inlines = [ImageInline]
    # what to display in thelist of Post objects
    list_display = (
        'title', 'pub_date',
    )
    list_filter = ['pub_date']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 160, 'rows': 90})}
    }


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
