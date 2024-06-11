from django.contrib import admin

# Register your models here.

from .models import Student, Employee, Customer, BankAccount

admin.site.register(Student)
admin.site.register(BankAccount)
admin.site.register(Employee)
admin.site.register(Customer)

