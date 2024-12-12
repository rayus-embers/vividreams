from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Video)
admin.site.register(VideoRating)
admin.site.register(ReportRating)
admin.site.register(ReportVideo)