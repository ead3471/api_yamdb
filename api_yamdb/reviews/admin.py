from django.contrib import admin
from .models import Title, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Comment)
