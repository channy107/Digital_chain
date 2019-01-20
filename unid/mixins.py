from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login


class ActiveOnlyMixin(PermissionRequiredMixin):

    permission_denied_message = '로그인이 필요합니다.'
    not_activated_message = ''
    not_activated_redirect = ''

    def get_permission_denied_message(self):
        """
        Override this method to override the permission_denied_message attribute.
        """
        return self.permission_denied_message
