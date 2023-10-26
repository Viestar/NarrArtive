from django.contrib import admin
from . import models


class StoryAdmin(admin.ModelAdmin):
    """Story representation on the admin panel"""

    list_display = ("author", "genre", "title", "body", "updated", "created")


class LikeAdmin(admin.ModelAdmin):
    """Story representation on the admin panel"""

    list_display = ("name", "likes")


class GenreAdmin(admin.ModelAdmin):
    """Story representation on the admin panel"""

    list_display = ("name", "description")


class CommentAdmin(admin.ModelAdmin):
    """Story representation on the admin panel"""

    list_display = ("commentor", "body", "created", "updated")


admin.site.register(models.Story, StoryAdmin)
admin.site.register(models.Like, LikeAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.User)
