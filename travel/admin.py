from django.contrib import admin
from .models import Destination, Booking,  ThingToExplore,  MustVisitPlace

admin.site.register(Destination)
admin.site.register(Booking)
admin.site.register(ThingToExplore)
admin.site.register(MustVisitPlace)
