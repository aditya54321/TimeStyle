from django.db import models
from django.utils import timezone
import uuid
from .validators import *
from .utils import *
    
class WatchDesign(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='watch_designs/')
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True) #,validators=[MobileRegexValidator()]
    password = models.CharField(max_length=100)
    registration_date = models.DateField(auto_now_add=True)
    last_login = models.DateField(default=timezone.now)
    is_administrator = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        # Clean first name and last name before saving
        self.first_name = clean_name(self.first_name)
        self.last_name = clean_name(self.last_name)

    def save(self, *args, **kwargs):
        # Clean first name and last name before saving
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "custome user"
        verbose_name_plural = "custome users"

    def __str__(self):
        return self.first_name

    
class Review(models.Model):
    watch_model = models.ForeignKey(WatchDesign, on_delete=models.CASCADE, related_name= "rating")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    description  = models.TextField(blank=True,null=True)
    rating = models.PositiveIntegerField(choices=((1,'1 star'),(2,'2 star'),(3,'3 star'),(4,'4 star'),(5,'5 star'),))
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_togather = ('user', 'watch_model')

    def __str__(self):
        return f"{self.name}'s {self.rating} - star rated"

class DesignDetails(models.Model):
    watch_design = models.OneToOneField(WatchDesign, on_delete=models.CASCADE)
    watch_face = models.CharField(max_length=100)
    strap = models.CharField(max_length=100)
    dial = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    movement = models.CharField(max_length=100,null=True)
    features = models.TextField(default='Water Resistant')

    def __str__(self):
        return f"{self.watch_design.name} - Details"
    
class seller(models.Model):
    name = models.CharField(max_length=50,default="Aditya Singh")
    address = models.CharField(max_length=150,default="Indra nagar, lucknow")
    phone = models.IntegerField(default='+91 8707465112')
    date = models.DateField(default=timezone.now)

class buyer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    pin_code = models.IntegerField(max_length=6)
    phone = models.IntegerField(max_length=13)
    purchase_date = models.DateField(default=timezone.now)



  
class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    design = models.ForeignKey(DesignDetails, on_delete=models.CASCADE)
    is_manufactured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    in_cart = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)


    


class Payment(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    razorpay_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Failed', 'Failed'), ('Successful', 'Successful')], default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return str(self.payment_id)
        return f"Cart {self.id} by {self.user.email}"
    

class OrderReceipt(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    total_quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cart.user.first_name} x {self.cart.design.watch_design.name} in Cart {self.payment.payment_id}"
    
