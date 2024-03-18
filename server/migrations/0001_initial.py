# Generated by Django 4.2.9 on 2024-03-15 06:00

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "uuid",
                    models.CharField(
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                        verbose_name="uuid",
                    ),
                ),
                ("nickname", models.CharField(max_length=25, verbose_name="攻击类型")),
                ("public_key", models.CharField(max_length=18, verbose_name="入侵时间")),
            ],
            options={
                "db_table": "user",
            },
        ),
    ]
