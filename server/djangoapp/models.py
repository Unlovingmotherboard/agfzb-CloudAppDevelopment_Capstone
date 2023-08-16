from django.db import models
from django.utils.timezone import now
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=90)
    # Add more fields later like color, condition, etc.
    def __str__(self):
        return f"{self.name} {self.description}"

class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ] #We will want to add more choices
    car_type = models.CharField(null=False, choices=CAR_TYPE_CHOICES, max_length=50)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealer_id = models.IntegerField(null=False)
    year = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.make} {self.name} {self.year}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
