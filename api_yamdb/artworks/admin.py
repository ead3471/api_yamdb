from django.contrib import admin
from .models import Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
