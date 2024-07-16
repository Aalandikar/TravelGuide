from django.contrib import admin
from .models import Destination, Booking, Enquiry, ThingToExplore, FamousRestaurant, MustVisitPlace

admin.site.register(Destination)
admin.site.register(Booking)
admin.site.register(Enquiry)
admin.site.register(ThingToExplore)
admin.site.register(FamousRestaurant)
admin.site.register(MustVisitPlace)
