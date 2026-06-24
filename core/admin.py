from django.contrib import admin

from .models import (
    UserProfile,
    Event,
    Booking,
    Payment,
    Review,
    Favorite,
    Movie,
    SportsEvent,
    Restaurant,
    Concert,
    MovieBooking,
    SportsBooking,
    RestaurantBooking,
    ConcertBooking,
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "promoter_type",
        "phone",
    )

    list_filter = (
        "role",
        "promoter_type",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone",
    )

    ordering = (
        "user__username",
    )

admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Favorite)
@admin.register(Movie)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "__str__",
    )

    ordering = ("id",)

class MovieAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "genre",
        "rating",
        "duration",
        "release_date",
        "show_time",
    )

    search_fields = (
        "title",
        "genre",
    )


@admin.register(SportsEvent)
class SportsEventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "venue",
        "event_date",
        "event_time",
        "ticket_price",
    )

    search_fields = (
        "title",
        "venue",
    )


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "rating",
        "location",
        "specialty",
        "opening_hours",
    )

    search_fields = (
        "title",
        "location",
    )


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "location",
        "concert_date",
        "concert_time",
        "price",
    )

    search_fields = (
        "title",
        "location",
    )
admin.site.register(SportsBooking)

@admin.register(ConcertBooking)
class ConcertBookingAdmin(admin.ModelAdmin):
    list_display = (
        "concert",
        "user",
        "seats",
        "amount",
        "booking_date",
    )

    list_filter = (
        "concert",
        "booking_date",
    )

    search_fields = (
        "user__username",
        "concert__title",
        "seats",
    )

    ordering = ("-booking_date",)

@admin.register(RestaurantBooking)
class RestaurantBookingAdmin(admin.ModelAdmin):

    list_display = (
        "restaurant",
        "user",
        "table_number",
        "booking_date",
    )

    search_fields = (
        "restaurant__title",
        "user__username",
        "table_number",
    )

    ordering = ("-booking_date",)

@admin.register(MovieBooking)
class MovieBookingAdmin(admin.ModelAdmin):

    list_display = (
        "movie",
        "user",
        "seats",
        "amount",
        "booking_date",
    )

    search_fields = (
        "movie__title",
        "user__username",
    )

    ordering = ("-booking_date",)


