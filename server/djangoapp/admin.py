from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

class CarModelInLine(admin.StackedInline):
    model = CarModel

class CarModelAdmin(admin.ModelAdmin): 
    list_display = ['name']

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInLine]

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)