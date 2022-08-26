from django.db import models


class ObjectType(models.Model):
    title = models.CharField(
        max_length=64,
        verbose_name="Тип",
        help_text="Тип объекта или организации.",
    )

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Тип"


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
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Описание объекта или организации, краткий обзор.",
        default="",
    )

    class Meta:
        verbose_name = "Фирма"
        verbose_name_plural = "Фирмы"
        constraints = (
            models.UniqueConstraint(
                fields=("title", "address"),
                name="unique_title_address",
            ),
        )


class Phone(models.Model):
    phone = models.CharField(blank=True, max_length=32, help_text="Контактный телефон.")
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"
