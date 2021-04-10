from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'listers', views.ListerViewSet)
router.register(r'renters', views.RenterViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'properties', views.PropertyViewSet)
router.register(r'amenities', views.AmenityViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'login', views.LoginViewSet, basename='Login')
router.register(r'searchproperties', views.PropertySearchViewSet, basename='Search')
router.register(r'renterreservations', views.ReservationSearchViewSet, basename='Search')
router.register(r'listerproperties', views.ListerPropertiesViewSet, basename='Search')
router.register(r'listerreservations', views.ListerReservationsViewSet, basename='Search')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]