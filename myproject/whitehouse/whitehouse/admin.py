from django.contrib import admin
from django.db import models
from .models import President, Authorities, Agencies, OrderType, Stories, Order, Deadline

# Register your models here.


class DeadlineInline(admin.TabularInline):
    model = Deadline
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [ DeadlineInline, ]
    list_display = ('president', 'sign_date', 'get_short_id', 'eo_proc_no', 'title', 'order_words')
    list_display_links = ('eo_proc_no', 'title')
    list_filter = ('president', 'order_type')

    def get_short_id(self, obj):
        return obj.order_type.short_type
        get_short_id.short_description = 'Type'

class StoriesAdmin(admin.ModelAdmin):
     readonly_fields = ('presto_id', 'story_date')

admin.site.register(President)
admin.site.register(Authorities)
admin.site.register(Agencies)
admin.site.register(OrderType)
admin.site.register(Stories, StoriesAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Deadline)

