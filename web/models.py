from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings

import datetime
from datetime import timedelta
from datetime import datetime as dt

today = datetime.date.today()

### Custom User Model Used Here

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


#### This is User Profile
class User(AbstractUser):
    user_gender = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    username = models.CharField(_('Username'), max_length=100, default='', unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, default='', choices=user_gender)
    # mobile = models.CharField(max_length=200, null=True)
    photo = models.ImageField(upload_to='users', default="/static/images/profile1.png", null=True, blank=True)
    country = models.CharField(max_length=200, null=True)
    bio = models.TextField(default='', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


#### This is user settings
class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    account_verified = models.BooleanField(default=False)
    verified_code = models.CharField(max_length=100, default='', blank=True)
    verification_expires = models.DateField(default=dt.now().date() + timedelta(days=settings.VERIFY_EXPIRE_DAYS))
    code_expired = models.BooleanField(default=False)
    recieve_email_notice = models.BooleanField(default=True)

#### User Payment History
class PayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    paystack_charge_id = models.CharField(max_length=100, default='', blank=True)
    paystack_access_code = models.CharField(max_length=100, default='', blank=True)
    payment_for = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

#### Membership
class Membership(models.Model):
    MEMBERSHIP_CHOICES = (
    	('Extended', 'Extended'), # Note that they are all capitalize//
    	('Advanced', 'Advanced'),
    	('Medium', 'Medium'),
        ('Basic', 'Basic'),
        ('Free', 'Free')
    )
    PERIOD_DURATION = (
        ('Days', 'Days'),
        ('Week', 'Week'),
        ('Months', 'Months'),
    )
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
    duration = models.PositiveIntegerField(default=7)
    duration_period = models.CharField(max_length=100, default='Day', choices=PERIOD_DURATION)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
       return self.membership_type

#### User Membership
class UserMembership(models.Model):
    user = models.OneToOneField(User, related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
    reference_code = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
       return self.user.username

@receiver(post_save, sender=UserMembership)
def create_subscription(sender, instance, *args, **kwargs):
	if instance:
		Subscription.objects.create(user_membership=instance, expires_in=dt.now().date() + timedelta(days=instance.membership.duration))


#### User Subscription
class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE, default=None)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
      return self.user_membership.user.username

@receiver(post_save, sender=Subscription)
def update_active(sender, instance, *args, **kwargs):
	if instance.expires_in < today:
		subscription = Subscription.objects.get(id=instance.id)
		subscription.delete()
