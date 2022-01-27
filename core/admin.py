from django.contrib import admin
from .models import (
    Movie,
    Comment,
    Vote
)

admin.site.register(Movie)
admin.site.register(Vote)
admin.site.register(Comment)
