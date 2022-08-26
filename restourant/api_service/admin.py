from django.contrib import admin

from .models import Phone, Organisation, ObjectType

EMPTY = "-пусто-"


class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    search_fields = ("title",)
    empty_value_display = EMPTY
    list_filter = ("title",)


class PhoneAdmin(admin.ModelAdmin):
    list_display = ("pk", "phone", "organisation")
    search_fields = ("phone", "organisation__title")
    empty_value_display = EMPTY
    list_filter = ("organisation__title",)


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "object_type", "address", "description")
    search_fields = (
        "title",
        "address",
        "object_type__title",
    )
    empty_value_display = EMPTY
    list_filter = ("object_type__title",)


admin.site.register(ObjectType, ObjectTypeAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Phone, PhoneAdmin)
