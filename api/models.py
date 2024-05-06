from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    location = models.CharField(max_length=30)
    about = models.TextField()
    type = models.CharField(max_length=30, choices=(
                                              ("IT","IT"),("Non IT","Non IT"), ("Electronics","Electronics"))
                                            )
    added_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

# class User(models.Model):
#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('user', 'User'),
#     ]

#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

#     def __str__(self):
#         return self.username
    
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    # user_role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(
        Group,
        related_name='api_user_groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='api_user_permissions'
    )

    def __str__(self):
        return self.username
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Email(models.Model):
    to = models.EmailField()
    desc = models.TextField()

    def __str__(self):
        return self.to + ":   " + self.desc