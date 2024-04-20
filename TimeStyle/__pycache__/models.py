from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.utils import timezone


# class UserManager(BaseUserManager):
#     def create_user(self, user_email, password):
#         user = self.model(email=self.normalize_email(user_email))
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

class WatchDesign(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='watch_designs/')  # You'll need to install and configure django-storages for production
    description = models.TextField()
    
    def __str__(self):
        return self.name

class DesignDetails(models.Model):
    watch_design = models.OneToOneField(WatchDesign, on_delete=models.CASCADE)
    watch_face = models.CharField(max_length=100)
    strap = models.CharField(max_length=100)
    dial = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.watch_design.name} - Details"

class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    registration_date = models.DateField(auto_now_add=True)
    last_login = models.DateField(default=timezone.now)
    is_administrator = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    # objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.USERNAME_FIELD


class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    design = models.ForeignKey(WatchDesign, on_delete=models.CASCADE)
    is_manufactured = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')],default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
