from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Page(models.Model):
    class PageName(models.TextChoices):
        Products_List = 'Products List'
        Marketing_List = 'Marketing List' 
        Order_List = 'Order List' 
        Media_Plans = 'Media Plans'
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

    def __str__(self):
        return self.name


class Permission(models.Model):
    VIEW = 'view'
    EDIT = 'edit'
    CREATE = 'create'
    DELETE = 'delete'

    PERMISSION_CHOICES = [
        (VIEW, 'View'),
        (EDIT, 'Edit'),
        (CREATE, 'Create'),
        (DELETE, 'Delete')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='permissions')
    permission_type = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ('user', 'page', 'permission_type')


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='comments', null=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} on {self.page.name}"


class CommentHistory(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='history')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    original_content = models.TextField()
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of {self.comment.id} by {self.modified_by.email if self.modified_by else 'Unknown'}"
