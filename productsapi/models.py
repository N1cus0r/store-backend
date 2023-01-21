from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models


def get_upload_path(instance, filename):
    return f'products/{instance.slug}' + '.' + filename.split('.')[-1]


class Product(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    slug = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to=get_upload_path, 
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])  
    time_created = models.DateTimeField(auto_now_add=True)
    sizes = ArrayField(models.CharField(max_length=4), null=True, blank=True)
    
    
    def create_slug(self):
        slug_lst = []
        for field in (self.brand, self.model, self.color):
            slug_lst.extend(list(map(lambda x: x.lower(), field.split())))
        return '-'.join(slug_lst)
    
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = self.create_slug()    
        return super(Product, self).save(*args, **kwargs)
    
    
    class Meta:
        ordering = ['-time_created']
    
    
    def __str__(self):
        return self.slug or ''
    
class OrderItem(models.Model):
    slug = models.CharField(max_length=200, null=True)
    size = models.CharField(max_length=4)
    price = models.IntegerField()


class Order(models.Model):
    #Identity
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20) 
    email = models.CharField(max_length=70)
    #Location
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    #Order Items
    # items = models.ManyToManyField(OrderItem)
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True)
    #Payment
    payment_type = models.CharField(max_length=4)
    total_price = models.IntegerField()     
    time_created = models.DateTimeField(auto_now_add=True)