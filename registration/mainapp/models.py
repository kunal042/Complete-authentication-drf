from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    # id =  models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                max_length=150, unique=True, validators=[UnicodeUsernameValidator()], verbose_name='username')
    first_name = models.CharField(
        blank=True, max_length=150, verbose_name='first name')
    last_name = models.CharField(
        blank=True, max_length=150, verbose_name='last name')
    email = models.EmailField(
        blank=True, max_length=254, verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='password')
    last_login = models.DateTimeField(
        blank=True, null=True, verbose_name='last login')

    # New phone field with a validator for numeric input
    phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$', message=_("Enter a valid phone number."))],
        help_text='Enter a valid phone number with 9 to 15 digits.'
    )

    # New image field for uploading user profile pictures
    image = models.ImageField(
        upload_to='/', blank=True, null=True, verbose_name='profile image')

    def __str__(self):
        return self.username
