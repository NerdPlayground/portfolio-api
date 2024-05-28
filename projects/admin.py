from .models import Project
from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):
    fields=[
        "name","link","start_date","end_date",
        "ongoing","description","objectives","tools"
    ]
    list_display=["name","link","start_date","ongoing","end_date"]
    search_fields=["name"]

    def save_model(self,request,obj,form,change):
        obj.user=request.user
        super().save_model(request,obj,form,change)
    
    def has_change_permission(self,request,obj=None):
        if obj: return obj.user==request.user
        return True

    def has_delete_permission(self,request,obj=None):
        if obj: return obj.user==request.user
        return True

admin.site.register(Project,ProjectAdmin)
