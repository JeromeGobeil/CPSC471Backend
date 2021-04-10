from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.template import Context

from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, ListerSerializer, RenterSerializer, PaymentSerializer, PropertySerializer, AmenitySerializer, LocationSerializer, ReservationSerializer, ReservationInfoSerializer, ReviewSerializer, DetailedPropertySerializer
from .models import User, Lister, Renter, Payment, Property, Amenity, Location, Reservation, Review

#Login View Set to check if a user can log in
class LoginViewSet(viewsets.ViewSet):

    def list(self, request, pk=None):
        user = None
        try:
            user = Lister.objects.get(username=request.GET["username"])
        except:
            user = None
        if user != None and user.password == request.GET["password"]:
            serializer = ListerSerializer(user)
            return Response(serializer.data)

        u = None
        try:
            u = Renter.objects.get( username=request.GET["username"])
        except:
            u = None
        if u != None and u.password == request.GET["password"]:
            s = RenterSerializer(u)
            return Response(s.data)
        
        return Response(status=400)

#Search viewset to get properties from a location
class PropertySearchViewSet(viewsets.ViewSet):

    def list(self, request, pk=None):
        location = get_object_or_404(Location.objects, cityName=request.GET["cityName"])
        serializer = DetailedPropertySerializer(location.properties, many=True, context={'request': request})
        return Response(serializer.data)

#Viewset that gets the renters reservations
class ReservationSearchViewSet(viewsets.ViewSet):

    def list(self, request, pk=None):
        renter = get_object_or_404(Renter.objects, username=request.GET["username"])
        serializer = ReservationInfoSerializer(renter.reservations, many=True, context={'request': request})
        return Response(serializer.data)

#Viewset that gets the listers properties
class ListerPropertiesViewSet(viewsets.ViewSet):

    def list(self, request, pk=None):
        lister = get_object_or_404(Lister.objects, username=request.GET["username"])
        serializer = DetailedPropertySerializer(lister.properties, many=True, context={'request': request})
        return Response(serializer.data)

#Viewset that gets the listers bookings
class ListerReservationsViewSet(viewsets.ViewSet):

    def list(self, request, pk=None):
        lister = get_object_or_404(Lister.objects, username=request.GET["username"])
        reservations = []
        for p in lister.properties.all():
            for r in p.reservations.all():
                reservations.append(r)
        serializer = ReservationInfoSerializer(reservations, many=True, context={'request': request})
        return Response(serializer.data)

#####################View Sets mainly for debug##########################3
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer

class ListerViewSet(viewsets.ModelViewSet):
    queryset = Lister.objects.all().order_by('pk')
    serializer_class = ListerSerializer

class RenterViewSet(viewsets.ModelViewSet):
    queryset = Renter.objects.all().order_by('pk')
    serializer_class = RenterSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('pk')
    serializer_class = PaymentSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('address')
    serializer_class = PropertySerializer

class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all().order_by('pk')
    serializer_class = AmenitySerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('pk')
    serializer_class = LocationSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by('pk')
    serializer_class = ReservationSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('pk')
    serializer_class = ReviewSerializer