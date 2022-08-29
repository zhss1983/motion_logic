from django.contrib import admin

from .models import ObjectType, Organisation, Owner, Phone

EMPTY = "-пусто-"


class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    search_fields = ("title",)
    empty_value_display = EMPTY


class PhoneAdmin(admin.ModelAdmin):
    list_display = ("pk", "phone", "organisation")
    search_fields = ("phone", "organisation__title")
    empty_value_display = EMPTY


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "object_type", "address", "latitude", "longitude", "description")
    search_fields = (
        "title",
        "address",
        "object_type__title",
    )
    empty_value_display = EMPTY
    list_filter = ("object_type__title",)


class OwnerAdmin(admin.ModelAdmin):
    list_display = ("pk", "owner", "organisation")
    empty_value_display = EMPTY


admin.site.register(ObjectType, ObjectTypeAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Owner, OwnerAdmin)
