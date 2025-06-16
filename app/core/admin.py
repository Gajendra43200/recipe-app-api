# Django admin customization vid 59
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _ 
# So if you do change the language of Django and you want to change it for everywhere in your project,
# then you can do it in the configuration and it means any way you use this translation shortcut here,
# it's going to automatically translate the text, which is really useful and this is just best practice.

from core import models

class UserAdmin(BaseUserAdmin):
    # Define the admin page for users 
    ordering = ['id']
    list_display = ['email', 'name'] 
    # It was using the default ordering, which comes with the base user admin, which includes a username
    # field which we don't have in our custom model.

    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        (   
           _('Permissions'),

           {
                'fields':(
                  'is_active',
                  'is_staff',
                  'is_superuser',
                )
           }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets =  (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
# Generate the migration for the recipe model: docker-compose run --rm app sh -c "python manage.py makemigrations vif 79-83"
# docker-compose run --rm app sh -c "python manage.py test"
# The migration should be applied automatically by the startup command that we can figure out in Docker
# Well, the Django test run out will automatically apply all the migrations every time you run it.
# PS C:\Users\INDIAN\Desktop\Udemy cource\recipe-app-api> docker-compose run --rm app sh -c "python manage.py startapp recipe"
