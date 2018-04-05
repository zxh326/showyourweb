from django.contrib import admin

# Register your models here.
class MyAdminSite(admin.AdminSite):
    site_header = 'Demo'  # 此处设置页面显示标题
    site_title = 'Demo'  # 此处设置页面头部标题
 
admin.site.site_header = 'Demo'
admin.site.site_title = 'Demo'