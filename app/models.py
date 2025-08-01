from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_super_admin = models.BooleanField(default=False)

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

class Page(models.Model):
    class PageName(models.TextChoices):
        Products_List = 'Products List '
        Marketing_List = 'Marketing List' 
        Order_List = 'Order List' 
        Media_Plans = 'Media Plans '
        Offer_Pricing_SKUs = 'Offer Pricing SKUs' 
        Clients = 'Clients' 
        Suppliers = 'Suppliers' 
        Customer_Support = 'Customer Support '
        Sales_Reports = 'Sales Reports'
        Finance_And_Accounting = 'Finance & Accounting'
        Default = 'NoNamePage'
    name = models.CharField(
        choices=PageName.choices,
        default=PageName.Default,
        max_length=50
    )

class PageComment(models.Model):
    page = models.ForeignKey(Page, related_name='Pcomment', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class PagePermission(models.Model):
    class AccessType(models.TextChoices):
        VIEW = 'view', 'View'
        EDIT = 'edit', 'Edit'
        CREATE = 'create', 'Create'
        DELETE = 'delete', 'Delete'

    user = models.ForeignKey(User, related_name='permissions', on_delete=models.CASCADE)
    page = models.ForeignKey(Page, related_name='permissions', on_delete=models.CASCADE)
    access_type = models.CharField(max_length=10, choices=AccessType.choices)

    class Meta:
        unique_together = ('user', 'page', 'access_type')
