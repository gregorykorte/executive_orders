from django.contrib import admin
from .models import President, Authorities, Agencies, OrderType, Stories, Order

# Register your models here.

admin.site.register(President)
admin.site.register(Authorities)
admin.site.register(Agencies)
admin.site.register(OrderType)
admin.site.register(Stories)
admin.site.register(Order)

