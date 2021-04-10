from django.db import models

#Basic user model
class User(models.Model):
    username = models.CharField(primary_key = True, max_length=60, default="")
    password = models.CharField(max_length=60, default="")
    firstName = models.CharField(max_length=60, default="")
    lastName = models.CharField(max_length=60, default="")
    branchNumber = models.CharField(max_length=60, default="")

    def __str__(self):
        return self.firstName + " " + self.lastName

#Lister model
class Lister(User):
    numOfListed = models.IntegerField(default=0)

#Renter model
class Renter(User):
    numOfReservations = models.IntegerField(default=0)

#Location model
class Location(models.Model):
    cityName = models.CharField(primary_key = True, max_length=60, default="")
    country = models.CharField(max_length=300, default="")

#Property Model
class Property(models.Model):
    address = models.CharField(primary_key = True, max_length=60, default="")
    name = models.CharField(max_length=60, default="")
    listerID = models.ForeignKey(Lister, on_delete=models.CASCADE, related_name = "properties")
    description = models.CharField(max_length=300, default="")
    price = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    cityName = models.ForeignKey(Location, on_delete=models.CASCADE, related_name = "properties")

#AmenityModel
class Amenity(models.Model):
    propertyAddress = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="amenities")
    amenityType = models.CharField(max_length=60, default="")
    description = models.CharField(max_length=300, default="")

#Reservation Model
class Reservation(models.Model):
    #reservationID = pk
    address = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, related_name="reservations")
    renterID = models.ForeignKey(Renter, on_delete=models.CASCADE, null=True, related_name="reservations")
    startTime = models.CharField( max_length=60, default="")
    endTime = models.CharField( max_length=60, default="")
    length = models.IntegerField(default=0)

#Payment model
class Payment(models.Model):
    renterID = models.ForeignKey(Renter, on_delete=models.CASCADE, null=True)
    listerID = models.ForeignKey(Lister, on_delete=models.CASCADE, null=True)
    listerBankNo = models.CharField(max_length=60, default="")
    renterBankNo = models.CharField(max_length=60, default="")
    amount = models.IntegerField(default=0)
    reservationID = models.OneToOneField(Reservation, on_delete=models.CASCADE, null=True, related_name="payment")

#Payment model
class Review(models.Model):
    reservationID = models.OneToOneField(Reservation, on_delete=models.CASCADE, null=True, related_name="review")
    comments = models.CharField(max_length=300, default="")
    rating = models.IntegerField(default=0)