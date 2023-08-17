from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=90)

    # Add more fields later like color, condition, etc.
    def __str__(self):
        return f"{self.name} {self.description}"


class CarModel(models.Model):
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    CAR_TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
    ]  # We will want to add more choices
    car_type = models.CharField(null=False, choices=CAR_TYPE_CHOICES, max_length=50)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealer_id = models.IntegerField(null=False)
    year = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.make} {self.name} {self.year}"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address  # Dealer address

        self.city = city  # Dealer city

        self.full_name = full_name  # Dealer Full Name

        self.id = id  # Dealer id

        self.lat = lat  # Location lat

        self.long = long  # Location long

        self.short_name = short_name  # Dealer short name

        self.st = st  # Dealer state

        self.zip = zip  # Dealer zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__( self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id,):
        
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Dealer review: " + self.review
