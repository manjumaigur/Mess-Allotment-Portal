from django.contrib import admin
from .models import Student, HostelOfficial, Manager

# Register your models here.
admin.site.register(Student)
admin.site.register(HostelOfficial)
admin.site.register(Manager)