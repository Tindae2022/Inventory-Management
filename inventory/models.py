from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum


class ProductManager(models.Manager):
    def in_stock(self):
        return self.filter(quantity_on_hand__gt=0)

    def low_stock(self):
        return self.filter(quantity_on_hand__gt=0, quantity_on_hand__lte=10)

    def high_stock(self):
        return self.filter(quantity_on_hand__gte=50)

    def expensive_products(self):
        return self.filter(unit_price__gt=200)

    def search_products(self, query):
        return self.filter(name__icontains=query)

    # def get_all_stock(self):
    # return self.all()

    def get_all_stock(self):
        return self.filter(quantity_on_hand__gt=0)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_on_hand = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2, editable=False, default=0)
    image = models.FileField(upload_to='uploads/')

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity_on_hand
        super().save(*args, **kwargs)

    def make_sale(self, quantity_sold):
        if quantity_sold <= self.quantity_on_hand:
            self.quantity_on_hand -= quantity_sold
            self.save()
            return True
        else:
            return False

    objects = ProductManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("product-detail", args=[str(self.id)])


class CustomerManager(models.Manager):
    def with_sales(self):
        return self.filter(sale__product__isnull=False)

    def search_customer_by_email(self, query):
        return self.filter(email__icontains=query)

    def search_customer_by_name(self, query):
        return self.filter(first_name__icontains=query)

    def get_all_customers(self):
        return self.all()


class Customer(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    objects = CustomerManager()

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse("customer-detail", args=[str(self.id)])


class SaleManager(models.Manager):
    def total_sales(self):
        return self.aggregate(total=Sum('quantity_sold'))['total']

    def recent_sales(self, days=30):
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return self.filter(sale_date__gte=cutoff_date)

    def sales_by_product(self):
        return self.values('product').annotate(total=Sum('quantity_sold')).order_by('quantity_sold')

    def get_all_sales(self):
        return self.all()


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.make_sale(self.quantity_sold)

    objects = SaleManager()

    class Meta:
        ordering = ["product"]

    def __str__(self):
        return f"{self.product} {self.quantity_sold}"

    def get_absolute_url(self):
        return reverse("sale-detail", args=[str(self.id)])


class AnalyticsManager(models.Manager):
    def top_selling_products(self, limit=10):
        return self.order_by('sales_count')[:limit]

    def highest_revenue_products(self, limit=10):
        return self.order_by('revenue')[:limit]

    def products_with_low_inventory(self):
        return self.filter(product__quantity_on_hand__lte=30)

    def product_with_high_inventory(self):
        return self.filter(product__quantity_on_hand__gte=100)

    def get_all_analysis(self):
        return self.all()


class Analytics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sales_count = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

    objects = AnalyticsManager()

    class Meta:
        ordering = ["product"]

    def __str__(self):
        return f"{self.product} {self.sales_count}"

    def get_absolute_url(self):
        return reverse("analytic-detail", args=[str(self.id)])
