from django.contrib import admin
from . models import Field, Activity, Alert
# Register your models here.
admin.site.register([Field, Activity, Alert])