from django.contrib import admin

from cloudviewer.models import Tenant
from .models import *
admin.site.register(Tenant)
admin.site.register(TenantConnections)
admin.site.register(TenantProducts)
admin.site.register(TenantApps)
admin.site.register(TenantUsers)
admin.site.register(TenantCloud)
admin.site.register(TenantServiceBoxName)
# Register your models here.
