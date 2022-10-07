from django.db import models
from django.contrib.auth.models import User



# Create your models here.
# ('fullname','email','message','admin_note','status')
STATUS = [
    ('new','new'),
    ('pending','pending'),
    ('processing','processing'),
    ('resolved','resolved')
    
]
class Contact(models.Model): 
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, default='a')
    email = models.EmailField(max_length=50)
    message = models.TextField()
    admin_note = models.TextField()
    status = models.CharField(max_length=50, choices= STATUS, default= 'new')
    message_date = models.DateTimeField(auto_now_add=True)
    admin_update = models.DateTimeField(auto_now=True)


    def _str_(self):
        return self.full_name

    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'



class Product(models.Model):
    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to= 'product', default='product/onion-rings-d1.jpg')
    price = models.IntegerField()
    max_quantity = models.IntegerField()
    min_quantity = models.IntegerField(default=False)
    display = models.BooleanField(default=False)
    latest = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner= models.BooleanField(default=False)
    dessert= models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    img = models.ImageField(upload_to='profile', default='profile/pix.jpg')

    def __str__(self):
        return self.user.username
        

    class Meta: 
        db_table = 'profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'



class Shopcart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    amount = models.IntegerField(blank=True, null=True)
    order_no = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name