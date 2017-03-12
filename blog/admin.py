from django.contrib import admin

from .models import Post, PostImage

class ImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    fieldsets = [
        ('Post Images',     {'fields': ['image_title', 'image']})
    ]

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    #used for organizing the admin editing interface
    fieldsets = [
        (None,               {'fields': ['title', 'slug', 'post', 'author']}),
        ('Date information', {'fields': ['pub_date',]}),
    ]
    inlines = [ImageInline]
    # what to display in thelist of Post objects
    list_display = (
        'title', 'pub_date',
    )
    list_filter = ['pub_date']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
