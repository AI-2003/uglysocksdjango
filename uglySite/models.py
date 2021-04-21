from django.db import models
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_delete


@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender,instance,field,instance_file_field)
            
def delete_file_if_unused(model,instance,field,instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)

# Create your models here.
class Product (models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    mainImage = models.ImageField(upload_to="uploads", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    categories = models.JSONField(null=True, blank=True)
    reviews = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    custom = models.BooleanField(default=False, null=True, blank=True)
    backImage = models.ImageField(upload_to="uploads", null=True, blank=True)

    def __str__(self):
        return self.name

class ProductImage (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads")

    def __str__(self):
        return self.product.name

class Order (models.Model):

    STATUS_OPTIONS = [
        ('RM', 'Remove'),
        ('PN', 'Pendiente'),
        ('EP', 'En proceso'),
        ('EN', 'Enviada'),
        ('RE', 'Recibida')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    received = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default='RM')
    products = models.JSONField(null=True, blank=True)
    #{  
    #   "name": ...,
    #    "email": ...
    #}

    def __str__(self):
        return str(self.id)

class Address(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField('Nombre(s)', max_length=100, null=True, blank=True)
    lastname = models.CharField('Apellidos', max_length=100, null=True, blank=True)
    country = models.CharField('País', max_length=150, null=True, blank=True)
    street = models.CharField('Calle y número (ext)', max_length=150, null=True, blank=True)
    innerNum = models.IntegerField("Número interior", null=True, blank=True)
    city = models.CharField('Ciudad', max_length=150, null=True, blank=True)
    region = models.CharField('Región/Provincia', max_length=150, null=True, blank=True)
    postalCode = models.IntegerField('Código Postal', null=True, blank=True)
    email = models.EmailField('Correo electrónico', max_length=254, null=True, blank=True)
    phone = models.CharField('Teléfono', max_length=150, null=True, blank=True)
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return self.street

class Review (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.CharField("Nombre *", max_length=100)
    review = models.TextField("Reseña *")
    email = models.EmailField("E-mail *")
    published = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.reviewer

class StripeReceipt (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    receipt = models.JSONField()

    def __str__(self):
        return str(self.id)

class CustomImage(models.Model):

    STATUS_OPTIONS = [
        ('RM', 'Remove'),
        ('PN', 'Pendiente'),
        ('EP', 'En proceso'),
        ('EN', 'Enviada'),
        ('RE', 'Recibida')
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    front = models.ImageField("Frente", upload_to="uploads/custom/", null=True, blank=True)
    back = models.ImageField("Atrás", upload_to="uploads/custom/", null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default='RM')

    def __str__(self):
        return str(self.uuid)