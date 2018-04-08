from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserFiles(models.Model):
    class Meta:
        verbose_name = "UserFiles"
        verbose_name_plural = "UserFiless"
        ordering = ['-last_submit_time']
    def info(self):
        result = {}
        if self.up_count <=0:
            result = {'id': self.id,
                      'name': self.user.last_name,
                      'pname': self.project_name, 
                      'time': self.last_submit_time,
                      'url': self.file_path}
        else:
            result = {'id': self.id,
                      'name': self.user.last_name,
                      'pname': self.project_name, 
                      'time': self.last_submit_time,
                      'url': self.file_path,
                      'upcount': self.up_count}
        return result

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
    up_count = models.IntegerField(
        default=0
    )


class UserUp(models.Model):

    class Meta:
        verbose_name = "UserUp"
        verbose_name_plural = "UserUps"

    project_id = models.ForeignKey(
        UserFiles,
        on_delete=models.CASCADE
        )
    up_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    up_time = models.DateTimeField(
        auto_now=True
    )
    