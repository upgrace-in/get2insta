from django.contrib import admin
from get2i import models

admin.site.register(models.ids_con)


class Insta_Idsinline(admin.TabularInline):
    model = models.ids

# class Instainline(admin.TabularInline):
#     model = models.username_used


@admin.register(models.users)
class InstaAdmin(admin.ModelAdmin):
    inlines = [
        Insta_Idsinline,
        # Instainline
    ]
