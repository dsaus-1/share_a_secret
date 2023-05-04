from django.contrib import admin

from secret.models import Secret


@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Secret._meta.fields]
