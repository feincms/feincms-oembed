# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CachedLookup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "hash",
                    models.CharField(
                        help_text="SHA-1 hash of the URL.",
                        unique=True,
                        max_length=40,
                        verbose_name="hash",
                    ),
                ),
                ("url", models.URLField(max_length=1000, verbose_name="URL")),
                ("_response", models.TextField(null=True, blank=True)),
                ("_httpstatus", models.PositiveIntegerField(null=True, blank=True)),
                (
                    "max_age_seconds",
                    models.PositiveIntegerField(
                        default=604800, verbose_name="Max. age in seconds"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
            ],
            options={
                "verbose_name": "cached lookup",
                "verbose_name_plural": "cached lookups",
            },
            bases=(models.Model,),
        ),
    ]
