from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
  GENDER_TYPE = (
     ('male', 'male'),
     ('female', 'female'),
     ('other', 'other'),
  )
  email = models.EmailField(_("email address"), unique=True, max_length=254)
  username = models.CharField(_("username"), unique=True, max_length=50)
  first_name = models.CharField(_("first name"), max_length=50)
  last_name = models.CharField(_("last name"), max_length=50)
  gender = models.CharField(choices = GENDER_TYPE,max_length=20, null=True, blank=True)
  phone = models.CharField(max_length=15, null=True, blank=True)


  is_staff = models.BooleanField(_("is staff"), default=False)
  is_active = models.BooleanField(_("is active"), default=True)
  date_joined = models.DateTimeField(_("date joined"), default=timezone.now)


  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  objects = CustomUserManager()

  def __str__(self):
      return self.email