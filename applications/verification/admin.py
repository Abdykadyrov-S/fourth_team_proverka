from django.contrib import admin
from applications.verification.models import CommonListPost, ListPost, CheckList

admin.site.register(CommonListPost)
admin.site.register(ListPost)
admin.site.register(CheckList)
