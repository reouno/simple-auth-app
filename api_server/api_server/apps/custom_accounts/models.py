import uuid as uuid_lib

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class GenderMaster(models.Model):
    """Gender master table"""
    id = models.CharField(primary_key=True, unique=True, blank=False, max_length=30, editable=False)

    def __str__(self):
        return f'{self.id}'


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where user_id is a unique identifiers.
    In many cases, user_id is email.
    If only a social account doesn't have email like LINE,
    user_id is not email but any id string that is used in the account.
    """

    def create_user(
            self, email: str = None, user_id: str = None, password: str = None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email and not user_id:
            raise ValueError(_('email or user_id must be set'))

        if email:
            # Use email as both user_id and email
            email = self.normalize_email(email)
            user = self.model(user_id=email, email=email, **extra_fields)
        else:
            # Use user_id only if email is not set
            user = self.model(user_id=user_id, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_id: str, password: str, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        user_id must be email.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(user_id, user_id, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Customized based on AbstractUser
    Use `email` as unique identifier instead of `username`
    """
    uuid = models.UUIDField(default=uuid_lib.uuid4,
                            primary_key=True, editable=False)

    # Email address can be used as user id and it's max length is 320.
    user_id = models.CharField(_('visible user id'), unique=True, max_length=320)

    # Not use `username`
    username = None

    first_name = models.CharField(_('first name'), max_length=64, blank=True)
    last_name = models.CharField(_('last name'), max_length=64, blank=True)
    email = models.EmailField(_('email address'), unique=True, null=True)

    password = models.CharField(_('password'), max_length=128, null=True,
                                help_text='Password is not set when signup with social account.')

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    birthday = models.DateField(_('birthday'), blank=True, null=True)
    gender = models.ForeignKey(to=GenderMaster, on_delete=models.PROTECT, null=True, blank=True)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    class Meta:
        """User model config"""
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        """clean"""
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
