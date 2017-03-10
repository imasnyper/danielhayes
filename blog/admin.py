from django.contrib import admin

from .models import Post, Author

# class AuthorInline(admin.TabularInline):
#     model = Author
#     extra = 1

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'post']}),
        ('Date information', {'fields': ['pub_date',]}),
    ]
    # inlines = [AuthorInline]
    list_display = (
        'title', 'pub_date',
    )
    list_filter = ['pub_date']
    search_fields = ['title']

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
