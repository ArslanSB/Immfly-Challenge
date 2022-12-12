from django.contrib import admin
from .models import Author, Channel, ChannelType, Content, ContentType, Genre, Language

# Register your models here.
admin.site.register(Author)
admin.site.register(Channel)
admin.site.register(ChannelType)
admin.site.register(Content)
admin.site.register(ContentType)
admin.site.register(Genre)
admin.site.register(Language)