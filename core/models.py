from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('promoter', 'Promoter'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    promoter_type = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('sports', 'Sports'),
        ('concert', 'Concert'),
        ('comedy', 'Comedy'),
        ('restaurant', 'Restaurant'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    venue = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Payment(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(max_length=100)

    transaction_id = models.CharField(max_length=200)

    payment_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20)

    def __str__(self):
        return self.transaction_id


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('sports', 'Sports'),
        ('restaurant', 'Restaurant'),
        ('event', 'Event'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200)
    date = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    genre = models.CharField(max_length=100)
    rating = models.CharField(max_length=20)
    cast = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    release_date = models.CharField(max_length=100)
    show_time = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class SportsEvent(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    venue = models.CharField(max_length=200)
    event_date = models.CharField(max_length=100)
    event_time = models.CharField(max_length=50)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Restaurant(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    rating = models.CharField(max_length=20)
    opening_hours = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Concert(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    location = models.CharField(max_length=200)
    concert_date = models.CharField(max_length=100)
    concert_time = models.CharField(max_length=50)
    price = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class MovieBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    seats = models.CharField(max_length=200)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class SportsBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(SportsEvent, on_delete=models.CASCADE)

    seats = models.CharField(max_length=200)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class RestaurantBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    table_number = models.CharField(max_length=50)
    amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0.00
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.title}"

class ConcertBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concert = models.ForeignKey(
        Concert,
        on_delete=models.CASCADE
    )

    seats = models.CharField(max_length=200)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.concert.title}"