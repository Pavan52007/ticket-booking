from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    # =========================
    # HOME & AUTH
    # =========================
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path(
    'standup-dashboard/',
    views.standup_dashboard,
    name='standup_dashboard'
),

    # =========================
    # DASHBOARD
    # =========================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('main-dashboard/', views.main_dashboard, name='main_dashboard'),

    # =========================
    # MAIN PAGES
    # =========================
    path('events/', views.events, name='events'),
    path('event-details/', views.event_details, name='event_details'),

    path('movies/', views.movies, name='movies'),
    path('sports/', views.sports, name='sports'),
    path('restaurants/', views.restaurants, name='restaurants'),
    path('concerts/', views.concerts, name='concerts'),
    path('offers/', views.offers, name='offers'),

    # =========================
    # SEARCH
    # =========================
    path('search/', views.search_result, name='search_result'),

    # =========================
    # BOOKING FLOW
    # =========================
    path('booking/', views.booking, name='booking'),
    path('booking-card/', views.booking_card, name='booking_card'),
    path('table-booking/', views.table_booking, name='table_booking'),

    # =========================
    # EVENT SEAT RESERVATION
    # =========================
    path('event-seat/', views.event_seat, name='event_seat'),
    path('event-checkout/', views.event_checkout, name='event_checkout'),

    # =========================
    # MY BOOKINGS
    # =========================
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('mybookings/', views.mybookings, name='mybookings'),
    path('ticket/', views.ticket, name='ticket'),

    # =========================
    # FAVORITES / WISHLIST
    # =========================
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/<int:id>/', views.favorite_detail, name='favorite_detail'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('add-favorite/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/<int:id>/', views.remove_favorite, name='remove_favorite'),

    # =========================
    # SPORTS
    # =========================
    path('sports/', views.sports, name='sports'),
    path('sport-ticket/', views.sport_ticket, name='sport_ticket'),
    path('sports-checkout/', views.sports_checkout, name='sports_checkout'),

    # =========================
    # CONCERTS
    # =========================
    path('concert-details/', views.concert_details, name='concert_details'),
    path(
        'concerts-checkout/<str:concert>/',
        views.concerts_checkout,
        name='concerts_checkout'
    ),

    # =========================
    # MOVIES
    # =========================
    path('movie-booking/', views.movie_booking, name='movie_booking'),
    path('theatre-seat/', views.theatre_seat, name='theatre_seat'),
    path('cinema-checkout/', views.cinema_checkout, name='cinema_checkout'),
    path('movie-details/', views.movie_details, name='movie_details'),

    # =========================
    # STANDUP COMEDY
    # =========================
    path('standup-comedy/', views.standup_comedy, name='standup_comedy'),
    path('standup-show/', views.standup_show, name='standup_show'),
    path('standup-checkout/', views.standup_checkout, name='standup_checkout'),
    path(
        'theatre-comedy/',
        views.theatre_comedy,
        name='theatre-comedy'
    ),

    # =========================
    # SETTINGS & NOTIFICATIONS
    # =========================
    path('settings/', views.settings_page, name='settings'),
    path('notifications/', views.notifications, name='notifications'),

    # =========================
    # LOGOUT
    # =========================
    path(
        'logout/',
        LogoutView.as_view(next_page='login'),
        name='logout'
    ),
    path(
    'admin-dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),
    path('restaurant-dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
]