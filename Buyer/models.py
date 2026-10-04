from django.db import models
from users.models import Users


# Create your models here.
class Buyer(models.Model):
  user=models.OneToOneField(
    Users,
    on_delete=models.CASCADE,
    related_name="buyer_profile"
  )
  name=models.CharField(max_length=100)
  email=models.EmailField(unique=True)
  age=models.IntegerField(blank=True,null=True)
  phone_number=models.CharField(max_length=20,unique=True)
  address=models.TextField(blank=True,null=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  gender=models.CharField(max_length=20,blank=True,null=True)
  
  #shipping address
  # shipping_state=models.CharField(max_length=100,blank=True,null=True)
  # shipping_city=models.CharField(max_length=100,blank=True,null=True)
  # shipping_postal_code=models.CharField(max_length=100,blank=True,null=True)
  shipping_address=models.TextField(blank=True,null=True)
  
  #billing address
  # billing_state=models.CharField(max_length=100,blank=True,null=True)
  # billing_city=models.CharField(max_length=100,blank=True,null=True)
  # billing_postal_code=models.CharField(max_length=100,blank=True,null=True)
  # billing_address=models.TextField(blank=True,null=True)
  
  # #ecommerce tracking
  # total_orders=models.BooleanField(default=False)
  # total_spent=models.DecimalField(max_digits=10,decimal_places=2,default=0)
  
  #profile image
  profile_pic=models.ImageField(upload_to='buyers/',blank=True,null=True)
  
  
  
  
  
  def __str__(self):
     return self.name
 
  
