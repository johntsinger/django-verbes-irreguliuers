from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from verbes_app.models import UserProfile, Verbe, Table


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        # self.model reference to this model (create_user)
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db) # using default db
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = None
    last_name = None

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username if self.username else self.email}' 


@receiver(post_save, sender=User, dispatch_uid="user_profile")
def create_user_profile(sender, instance, **kwargs):
    """Create UserProfile for each created User"""
    user_profile, create = UserProfile.objects.get_or_create(user=instance)
    verbes = list(Verbe.objects.all())
    user_profile.verbes.add(*verbes)
    tables = list(Table.objects.filter(default=True))
    user_profile.tables.add(*tables)