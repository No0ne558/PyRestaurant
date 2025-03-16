from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models import JSONField

class UserManager(BaseUserManager):
    def create_user(self, number_id, password=None, **extra_fields):
        if not number_id:
            raise ValueError("Users must have a number ID")
        user = self.model(number_id=number_id, **extra_fields)
        if password:
            user.set_password(password)  # Only if password is provided
        else:
            user.set_unusable_password()  # No password required for normal users
        user.save(using=self._db)
        return user

    def create_superuser(self, number_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(number_id, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    number_id = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'number_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.number_id)

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    is_open = models.BooleanField(default=True)
    opened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    check_number = models.PositiveIntegerField()  # Remove default!

    def total_amount(self):
        return sum(item.total_price() for item in self.orderitem_set.all())

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.menu_item.price * self.quantity

class CheckCounter(models.Model):
    current_number = models.PositiveIntegerField(default=0)

    @classmethod
    def next_check_number(cls):
        counter, created = cls.objects.get_or_create(id=1)  # Single row
        counter.current_number += 1
        counter.save()
        return counter.current_number

class CheckHistory(models.Model):
    check_number = models.PositiveIntegerField()
    table_number = models.PositiveIntegerField()
    opened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opened_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    items_data = JSONField(blank=True, null=True)  # 🔥 This will hold items data (menu item id + quantity)

    def __str__(self):
        return f"Check #{self.check_number} - Table {self.table_number} - Opened by {self.opened_by.number_id}"