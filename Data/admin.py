from django.contrib import admin
from .models import DBSource, TagGroup, Tag
# Register your models here.

class DBSourceAdmin(admin.ModelAdmin):
    fields = ['name', 'address', 'port', 'database', 'user', 'password']
    list_display = ('name', 'address', 'port', 'database', 'user',)

class TagGroupAdmin(admin.ModelAdmin):
    fields = ['name']

class TagAdmin(admin.ModelAdmin):
    fields = ['name', 'sql', 'group', 'dbsource']
    list_display = ('name', 'group', 'dbsource')

# admin.site.register(DBSource, DBSourceAdmin)
# admin.site.register(TagGroup, TagGroupAdmin)
# admin.site.register(Tag, TagAdmin)