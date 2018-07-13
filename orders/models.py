from django.db import models
from products.models import Product
from django.db.models.signals import post_save

class Status(models.Model):
    name = models.CharField(max_length=16, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Status: %s" % self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "ORDER Statuses"


class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_name = models.CharField(max_length=128, blank=True, default=None)
    customer_email = models.EmailField(blank=True, default=None)
    customer_phone = models.CharField(max_length=48, blank=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, default=None)
    comments = models.TextField(blank=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Order: %s %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        super(Order, self).save()


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, default=None, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    customer_name = models.CharField(max_length=128, blank=True, default=None)
    customer_email = models.EmailField(blank=True, default=None)
    customer_phone = models.CharField(max_length=48, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = "Product in order"
        verbose_name_plural = "Products in order"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = self.number * self.price_per_item

        super(ProductInOrder, self).save()


def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = "Product in shopping cart"
        verbose_name_plural = "Products in shopping cart"

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.number) * self.price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)

