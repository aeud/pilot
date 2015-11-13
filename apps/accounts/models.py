from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import pytz, hashlib, uuid
from urllib.parse import urlencode

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class BigQueryProject(models.Model):
    project_id  = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class Account(models.Model):
    name                  = models.CharField(max_length=255, unique=True)
    created_at            = models.DateTimeField(auto_now_add=True)
    updated_at            = models.DateTimeField(auto_now=True)
    is_active             = models.BooleanField(default=True)
    credentials           = models.TextField(null=True)
    bq_project            = models.OneToOneField(BigQueryProject, null=True)
    aws_access_key_id     = models.CharField(max_length=255, null=True)
    aws_secret_access_key = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class User(AbstractBaseUser):
    email           = models.EmailField('email address', unique=True, db_index=True)
    joined          = models.DateTimeField(auto_now_add=True)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    first_name      = models.CharField(max_length=255, null=True)
    last_name       = models.CharField(max_length=255, null=True)
    handle          = models.CharField(max_length=255, null=True, unique=True)
    avatar_url      = models.CharField(max_length=255, null=True)
    ga_uuid         = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    account         = models.ForeignKey(Account, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.first_name if self.first_name is not None else self.email