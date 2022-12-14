# Generated by Django 4.1 on 2022-08-28 11:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_service", "0002_alter_objecttype_options_organisation_latitude_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Owner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.AlterModelOptions(
            name="organisation",
            options={},
        ),
        migrations.RemoveConstraint(
            model_name="organisation",
            name="unique_title_address",
        ),
        migrations.AddField(
            model_name="owner",
            name="organisation",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="owner2organisation",
                to="api_service.organisation",
            ),
        ),
        migrations.AddField(
            model_name="owner",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="organisation2owner",
                to="api_service.organisation",
            ),
        ),
    ]
