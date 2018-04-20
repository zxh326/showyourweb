from django.contrib import admin
from show.models import UserFiles
# Register your models here.

class UserFilesAdmin(admin.ModelAdmin):
    '''
        Admin View for UserFiles
    '''
    list_display = ('user','project_name', 'file_path', 'up_count', 'last_submit_time')
    list_filter = ('is_ective', 'last_submit_time')
    readonly_fields = ('up_count','submit_count')


admin.site.register(UserFiles, UserFilesAdmin)

admin.site.site_header = '人机交互项目项目管理中心'
admin.site.site_title = '人机交互项目项目管理中心'