from django.contrib import admin
from .models import *
# Register your models here.


#Inlines
class ImageInLine(admin.TabularInline):
    model = Image
    extra = 1

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','publish','status']
    ordering = ['title','publish']
    list_filter = ['status','author','publish']
    search_fields = ['title','description']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {"slug" : ['title']}
    list_editable = ['status']
    list_display_links = ['author']
    inlines = [ImageInLine,CommentInLine]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name','subject','phone']

@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ['post','name','created','active']
    list_filter = ['active','created','updated']
    search_fields = ['name','body']
    list_editable = ['active']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post','title','created']