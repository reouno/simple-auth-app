"""Customize social account adapter of django-allauth"""

from allauth.account.utils import user_email, user_field, user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import valid_email_or_none


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom social account adapter"""

    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.

        For convenience, we populate several common fields.

        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.

        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.

        Based on this code:
        https://github.com/pennersr/django-allauth/blob/422c3f5852c271cc69662757b9b5ce3792c1d585/allauth/socialaccount/adapter.py#L87
        """
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        name = data.get("name")
        user = sociallogin.user
        user_username(user, valid_email_or_none(email) or username or "")
        user_email(user, valid_email_or_none(email) or "")
        name_parts = (name or "").partition(" ")
        user_field(user, "first_name", first_name or name_parts[0])
        user_field(user, "last_name", last_name or name_parts[2])
        return user
