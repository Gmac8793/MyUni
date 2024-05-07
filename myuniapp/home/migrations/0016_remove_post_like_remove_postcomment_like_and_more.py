# Generated by Django 4.2.10 on 2024-05-06 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("home", "0015_rename_ryplyimage_replyimage_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="post", name="like",),
        migrations.RemoveField(model_name="postcomment", name="like",),
        migrations.AddField(
            model_name="postcomment",
            name="likes",
            field=models.ManyToManyField(
                default=0, related_name="likedcomments", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="LikedPost",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.post"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                default=0,
                related_name="likedposts",
                through="home.LikedPost",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
