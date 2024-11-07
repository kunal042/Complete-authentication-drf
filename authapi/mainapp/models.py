from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name,  password=None, password2=None, phone=None, address=None, image=None):
        """
        Creates and saves a User with the given email, name, tc, password, phone, address, and image.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            address=address,
            image=image
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name, password=None):
        """
        Creates and saves a superuser with the given email, name, and password.
        """
        user = self.create_user(
            email=email,
            name=name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    name = models.CharField(max_length=200, verbose_name='Full Name')
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
