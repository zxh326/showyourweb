from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserFiles(models.Model):
    class Meta:
        verbose_name = "UserFiles"
        verbose_name_plural = "UserFiless"
        ordering = ['-last_upload_time']

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )

    upload_name = models.CharField(
        max_length=155,
        )
    upload_files = models.CharField(
        max_length=155,
        verbose_name='文件',
        )
    last_upload_time = models.DateTimeField(
        auto_now=True
    )
    upload_count = models.IntegerField(
        default=1
        )