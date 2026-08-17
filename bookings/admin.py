from django.contrib import admin
from .models import Table, Customer, Reservation

admin.site.register(Table)
admin.site.register(Customer)
admin.site.register(Reservation)