from django.contrib import admin

# Register your models here.
# from account.models import User
from account.models import User

admin.site.register(User)

# ###for middleware
# from account.models import User, Userstatus
# admin.site.register(Userstatus)
