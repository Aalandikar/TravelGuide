from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    best_time_to_visit = models.CharField(max_length=100)
    price_adult = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    price_child = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    

    def __str__(self):
        return self.name

class ThingToExplore(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='things_to_explore')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='things_to_explore/')

    def __str__(self):
        return self.name

class FamousRestaurant(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='famous_restaurants')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='famous_restaurants/')

    def __str__(self):
        return self.name

class MustVisitPlace(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='must_visit_places')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='must_visit_places/')

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"
    

class Enquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    message = models.TextField()
    phone = models.CharField(max_length=15, default='') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry by {self.user.username} for {self.destination.name}"
