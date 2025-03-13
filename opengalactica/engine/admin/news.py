from django.contrib import admin
from engine.models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ["slug", "title", "server_time"]
    ordering = ("server_time","title")


admin.site.register(News, NewsAdmin)