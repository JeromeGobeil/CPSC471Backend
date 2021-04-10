
from rest_framework import serializers

from .models import User, Lister, Renter, Payment, Property, Amenity, Location, Reservation, Review

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',"firstName", "lastName", "branchNumber",)

class ListerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lister
        fields = ('username', 'password',"firstName", "lastName", "branchNumber","numOfListed")

class RenterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Renter
        fields = ('username', 'password',"firstName", "lastName", "branchNumber","numOfReservations")

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = ('pk',"renterID", "listerID", "amount", "listerBankNo", "renterBankNo", "reservationID" )
    
    #Custom create method to get Branch numbers
    def create(self, validated_data):
        p = Payment.objects.create(**validated_data)
        p.listerBankNo = p.listerID.branchNumber
        p.renterBankNo = p.renterID.branchNumber
        return p

class AmenitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Amenity
        fields = ('propertyAddress', "amenityType", "description", )

class PropertySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Property
        fields = ('address', "cityName", "listerID", "description", "price", "capacity", "name", )

class DetailedPropertySerializer(serializers.HyperlinkedModelSerializer):
    amenities = AmenitySerializer(many=True)

    class Meta:
        model = Property
        fields = ('address', "cityName", "listerID", "description", "price", "capacity", "name", "amenities")

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('cityName', "country", )

class ReviewSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Review
        fields = ('reservationID', "comments", "rating",)

class ReservationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Reservation
        fields = ('address', "renterID", "startTime", "endTime", "length",)

    #Custom create method to automatically create a payment
    def create(self, validated_data):
        r = Reservation.objects.create(**validated_data)

        p = Payment.objects.create()
        p.renterID = r.renterID
        p.listerID = r.address.listerID
        p.listerBankNo = r.address.listerID.branchNumber
        p.renterBankNo = r.renterID.branchNumber
        p.reservationID = r
        #TODO: fix how price is calculated
        p.amount = r.address.price * r.length
        p.save()
        
        return r

class ReservationInfoSerializer(serializers.HyperlinkedModelSerializer):
    payment = PaymentSerializer()
    review = ReviewSerializer()
    address = DetailedPropertySerializer()

    class Meta:
        model = Reservation
        fields = ('pk', 'address', "renterID", "startTime", "endTime", "length", "payment", "review")

