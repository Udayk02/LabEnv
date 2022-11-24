from django.contrib import admin
from .models import ClassRoom,Assignment,Answer,Poll

# Register your models here.
admin.site.register(ClassRoom)
admin.site.register(Assignment)
admin.site.register(Answer)
admin.site.register(Poll)
