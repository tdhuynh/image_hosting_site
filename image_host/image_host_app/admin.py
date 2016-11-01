from django.contrib import admin
from image_host_app.models import Post, Comment, Profile

admin.site.register([Post, Comment, Profile])
