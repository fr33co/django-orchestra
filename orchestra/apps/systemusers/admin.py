import textwrap

from django import forms
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.admin.util import unquote
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.safestring import mark_safe

from orchestra.admin import ExtendedModelAdmin, ChangePasswordAdminMixin
from orchestra.admin.utils import wrap_admin_view
from orchestra.apps.accounts.admin import SelectAccountAdminMixin
from orchestra.forms import UserCreationForm, UserChangeForm

from . import settings
from .actions import grant_permission
from .filters import IsMainListFilter
from .models import SystemUser


class SystemUserAdmin(ChangePasswordAdminMixin, SelectAccountAdminMixin, ExtendedModelAdmin):
    list_display = ('username', 'account_link', 'shell', 'display_home', 'display_active', 'display_main')
    list_filter = ('is_active', 'shell', IsMainListFilter)
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'account_link', 'is_active')
        }),
        (_("System"), {
            'fields': ('shell', ('home', 'directory'), 'groups'),
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('account_link', 'username', 'password1', 'password2')
        }),
        (_("System"), {
            'fields': ('shell', ('home', 'directory'), 'groups'),
        }),
    )
    search_fields = ['username']
    readonly_fields = ('account_link',)
    change_readonly_fields = ('username',)
    filter_horizontal = ('groups',)
    filter_by_account_fields = ('groups',)
    add_form = UserCreationForm
    form = UserChangeForm
    ordering = ('-id',)
    actions = (grant_permission,)
    change_view_actions = actions
    
    def display_active(self, user):
        return user.active
    display_active.short_description = _("Active")
    display_active.admin_order_field = 'is_active'
    display_active.boolean = True
    
    def display_main(self, user):
        return user.is_main
    display_main.short_description = _("Main")
    display_main.boolean = True
    
    def display_home(self, user):
        return user.get_home()
    display_home.short_description = _("Home")
    display_home.admin_order_field = 'home'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(SystemUserAdmin, self).get_form(request, obj=obj, **kwargs)
        duplicate = lambda n: (n, n)
        if obj:
            # Has to be done here and not in the form because of strange phenomenon
            # derived from monkeypatching formfield.widget.render on AccountAdminMinxin,
            # don't ask.
            formfield = form.base_fields['groups']
            formfield.queryset = formfield.queryset.exclude(id=obj.id)
            username = obj.username
            choices=(
                duplicate(self.account.main_systemuser.get_home()),
                duplicate(obj.get_home()),
            )
        else:
            username = '<username>'
            choices=(
                duplicate(self.account.main_systemuser.get_home()),
                duplicate(SystemUser(username=username).get_home()),
            )
        form.base_fields['home'].widget = forms.Select(choices=choices)
        if obj and (obj.is_main or obj.has_shell):
            # hidde home option for shell users
            form.base_fields['home'].widget = forms.HiddenInput()
            form.base_fields['directory'].widget = forms.HiddenInput()
        else:
            # Some javascript for hidde home/directory inputs when convinient
            form.base_fields['shell'].widget.attrs = {
                'onChange': textwrap.dedent("""\
                    field = $(".form-row.field-home.field-directory");
                    if ($.inArray(this.value, %s) < 0) {
                        field.addClass("hidden");
                    } else {
                       field.removeClass("hidden");
                    };""" % str(list(settings.SYSTEMUSERS_DISABLED_SHELLS)))
            }
        form.base_fields['home'].widget.attrs = {
            'onChange': textwrap.dedent("""\
                field = $(".field-box.field-directory");
                if (this.value.search("%s") > 0) {
                   field.addClass("hidden");
                } else {
                   field.removeClass("hidden");
                };""" % username)
        }
        return form
    
    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_main:
            return False
        return super(SystemUserAdmin, self).has_delete_permission(request, obj=obj)


admin.site.register(SystemUser, SystemUserAdmin)
