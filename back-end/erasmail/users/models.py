from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(max_length=20, default="N/A")
    connected_count = models.PositiveIntegerField(default=0, help_text="Number of times the user connected to ErasMail")

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

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'

# class Success(models.Model):
#     user = models.ForeignKey(CustomUser, related_name='success', on_delete=models.CASCADE)
#     name = models.CharField(max_length=256, unique=True, blank=True)
#     done = models.BooleanField(default=False)