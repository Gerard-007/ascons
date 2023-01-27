from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from accounts.models import User


class MyAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    model = User
    add_form = UserCreationForm
    # readonly_fields = (
    #     'balance',
    # )
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'phone', 'date_joined', 'is_staff', 'is_school_staff', 'is_active', 'is_lecturer', 'is_student',)
    list_filter = ('is_school_staff', 'is_lecturer', 'is_student', 'date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ('avatar', 'bio',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password', 'password2')}
         ),
    )
    search_fields = ('username',)
    ordering = ('date_joined',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, MyAdmin)
