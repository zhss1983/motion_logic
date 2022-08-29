from django.db import models
from django.db.models import Deferrable, UniqueConstraint


class ObjectType(models.Model):
    title = models.CharField(
        max_length=64,
        verbose_name="Тип",
        help_text="Тип объекта или организации.",
    )

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Тип"

    def __str__(self):
        return self.title


class Organisation(models.Model):
    title = models.CharField(
        max_length=172,
        verbose_name="Название",
        help_text="Название объекта или организации.",
    )
    object_type = models.ForeignKey(
        ObjectType,
        help_text="Тип объекта или организации.",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=256,
        verbose_name="Адрес",
        help_text="Адрес объекта или организации.",
    )
    latitude = models.FloatField(
        verbose_name="Широта", help_text="Широта на которой находится объёект или организация.", default=0
    )
    longitude = models.FloatField(
        verbose_name="Долгота", help_text="Долгота на которой находится объёект или организация.", default=0
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Описание объекта или организации, краткий обзор.",
        default="",
    )

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.title


class Owner(models.Model):
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="owner2organisation",
        help_text="Указатель на подчинённые объекты и организации.",
        verbose_name="Подчинённый",
    )
    owner = models.ForeignKey(
        Organisation,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="organisation2owner",
        help_text="Указатель на владельцев.",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Подчинённость"
        verbose_name_plural = "Подчинённость"
        UniqueConstraint(
            name="unique_organisation_owner",
            fields=["organisation", "owner"],
            deferrable=Deferrable.DEFERRED,
        )

    def __str__(self):
        return self.owner + " -> " + self.organisation


class Phone(models.Model):
    phone = models.CharField(blank=True, max_length=32, help_text="Контактный телефон.")
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )
    UniqueConstraint(
        name="unique_organisation_phone",
        fields=["organisation", "phone"],
        deferrable=Deferrable.DEFERRED,
    )

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"

    def __str__(self):
        return str(self.phone)
