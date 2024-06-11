from django.db import models


# Create your models here.

class Person(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone_number = models.IntegerField()


# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

class Student(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.CharField(max_length=50, default="0")
    password = models.CharField(max_length=20, default="0")

    def __str__(self):
        return f"{self.fname}  {self.lname}"


class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
        ('salary', 'Salary'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)


# -----------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

class Employee(models.Model):
    name = models.CharField(max_length=20)
    photo = models.FileField(upload_to='images')

    def __str__(self):
        return self.name


class Customer(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)

    def __str__(self):
        return self.fname
