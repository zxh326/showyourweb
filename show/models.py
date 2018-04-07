from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserFiles(models.Model):
    class Meta:
        verbose_name = "UserFiles"
        verbose_name_plural = "UserFiless"
        ordering = ['-last_submit_time']

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    is_ective = models.IntegerField(
        default=0
        )
    project_name = models.CharField(
        max_length=155,
        )
    file_path = models.CharField(
        max_length=155,
        verbose_name='文件',
        )
    last_submit_time = models.DateTimeField(
        auto_now=True
    )
    submit_count = models.IntegerField(
        default=1
        )