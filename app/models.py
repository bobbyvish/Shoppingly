from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.db.models.base import Model
from django.template.defaultfilters import slugify


STATE_CHOIES = (
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh ", "Arunachal Pradesh "),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu and Kashmir ", "Jammu and Kashmir "),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Chandigarh", "Chandigarh"),
    ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"),
    ("Daman and Diu", "Daman and Diu"),
    ("Lakshadweep", "Lakshadweep"),
    ("National Capital Territory of Delhi", "National Capital Territory of Delhi"),
    ("Puducherry", "Puducherry"))


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOIES, max_length=50)

    def __str__(self):
        return str(self.id)


class Category(models.Model):
    category_name = models.CharField(primary_key=True, max_length=30)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.category_name


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    offer = models.IntegerField(default=0)
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category_name = models.ForeignKey(
        to='Category', on_delete=models.CASCADE, default=1)
    product_image = models.ImageField(blank=True)

    def __str__(self):
        return str(self.id)

    def save(self):
        self.discounted = (self.selling_price * self.offer)/100
        self.discounted_price = self.selling_price - self.discounted
        return super(Product, self).save()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='productimg')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=50, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
