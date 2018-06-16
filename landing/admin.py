from django.contrib import admin
from .models import *

class SubscriberAdmin(admin.ModelAdmin):
    # list_display = ["name", "email"] # split table to fields
    list_display = [field.name for field in Subscriber._meta.fields] # all fields name
    list_filter = ["name",]
    search_fields = ["name", "email"]
    # inlines = [FieldMappingInline]
    # fields = ["email"]
    # exclude = ["email"] # excludes field email
    class Meta:
        model = Subscriber

admin.site.register(Subscriber, SubscriberAdmin) # register model Subscribers