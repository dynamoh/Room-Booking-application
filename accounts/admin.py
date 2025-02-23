from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','name', 'is_admin','customer')
    list_filter = ('is_admin','customer','manager')
    fieldsets = (
        (None, {'fields': ('email', 'password','name')}),
        ('Personal info', {'fields': ('customer','manager')}),
        ('Permissions', {'fields': ('is_admin','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','name')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email','name')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.site_header = 'Room Booking'
