from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .data import MOVIES, CONCERTS, RESTAURANTS, SPORTS, OFFERS, DASHBOARD

from .models import (
    Favorite,
    UserProfile,
    Movie,
    Restaurant,
    SportsEvent,
    Concert,
    Booking,
    MovieBooking,
    SportsBooking, 
    ConcertBooking,
    MovieBooking
)
# =========================
# BASIC PAGES
# =========================

def home(request):
    return render(request, 'home.html')

from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role != "admin":
        return redirect("dashboard")

    return render(request, "admin_dashboard.html")

from django.contrib.auth import authenticate, login
from .models import UserProfile

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            try:
                profile = UserProfile.objects.get(user=user)

                print("ROLE =", profile.role)
                print("PROMOTER TYPE =", profile.promoter_type)

                if profile.role == "customer":
                    return redirect("dashboard")

                elif profile.role == "admin":
                    return redirect("admin_dashboard")

                    
                elif profile.role == "promoter":
                    if profile.promoter_type == "standup_comedy_owner":
                        return redirect("standup_dashboard")
                        
                    elif profile.promoter_type == "restaurant_owner":
                        return redirect("restaurant_dashboard")

                    elif profile.promoter_type == "stadium_owner":
                        return redirect("stadium_dashboard")
                        
                    elif profile.promoter_type == "theatre_owner":
                        return redirect("theatre_dashboard")
                        
                    elif profile.promoter_type == "music_concert_owner":
                        return redirect("concerts_dashboard")
                        
                return redirect("dashboard")

            except UserProfile.DoesNotExist:
                return redirect("dashboard")

        return render(
            request,
            "login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "login.html")

# ✅ FIXED: now saves user data in session

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        role = request.POST.get("role", "customer")
        promoter_type = request.POST.get("promoter_type", "")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            phone=phone,
            role=role,
            promoter_type=promoter_type
        )

        return redirect("login")

    return render(request, "register.html")
def dashboard(request):
    return render(request, 'main_dashboard.html', {
        "data": DASHBOARD
    })


# =========================
# PROFILE (NEW - REQUIRED FOR YOUR ISSUE)
# =========================

def profile(request):
    user = request.session.get('user')

    return render(request, 'profile.html', {
        "user": user
    })

from .models import Event
def events(request):
    events = Event.objects.all()

    print("EVENT COUNT =", events.count())

    return render(
        request,
        "events.html",
        {
            "events": events
        }
    )

def event_details(request):
    return render(request, 'event_details.html')

from .models import Movie

def movies(request):

    movies = Movie.objects.all()

    return render(
        request,
        'movies.html',
        {
            "movies": movies
        }
    )
def concerts(request):

    concerts = Concert.objects.all()

    return render(
        request,
        "concerts.html",
        {
            "concerts": concerts
        }
    )


from .models import SportsEvent

def sports(request):

    sports = SportsEvent.objects.all()

    print("SPORTS COUNT =", sports.count())

    return render(
        request,
        'sports.html',
        {
            "sports": sports
        }
    )



def restaurants(request):

    restaurants = Restaurant.objects.all()

    print("RESTAURANTS COUNT =", restaurants.count())

    return render(
        request,
        'restaurants.html',
        {
            'restaurants': restaurants
        }
    )


def offers(request):
    return render(request, 'offers.html', {
        "offers": OFFERS
    })


# =========================
# BOOKINGS
# =========================


def table_booking(request):

    restaurant_id = request.GET.get("restaurant")

    print("URL RESTAURANT ID =", restaurant_id)

    request.session["restaurant_id"] = restaurant_id

    restaurant = Restaurant.objects.get(id=restaurant_id)

    return render(
        request,
        "table-booking.html",
        {
            "restaurant": restaurant
        }
    )


def booking(request):
    restaurant = request.GET.get('restaurant', 'Restaurant')

    return render(request, 'booking_card.html', {
        'restaurant': restaurant
    })

def sports_checkout(request):

    if request.method == "POST":
        print("POST DATA =", request.POST)

        seats = request.POST.get("seats")
        amount = request.POST.get("amount")

        booking = Booking.objects.create(
            user=request.user,
            event_name="CSK vs MI",
            seats=seats,
            amount=amount,
            status="Confirmed"
        )

        available_seats = Seat.objects.filter(
            event_name="CSK vs MI",
            is_booked=False
        )[:int(seats)]

        for seat in available_seats:
            seat.is_booked = True
            seat.booking = booking
            seat.save()

        request.session["amount"] = amount

        return redirect("payment")

    return render(
        request,
        "sports-checkout.html"
    )

def my_bookings(request):

    if not request.user.is_authenticated:
        return redirect("login")

    movie_bookings = MovieBooking.objects.filter(
        user=request.user
    ).order_by("-booking_date")

    restaurant_bookings = RestaurantBooking.objects.filter(
        user=request.user
    ).order_by("-booking_date")

    concert_bookings = ConcertBooking.objects.filter(
        user=request.user
    ).order_by("-booking_date")

    return render(
        request,
        "mybookings.html",
        {
            "movie_bookings": movie_bookings,
            "restaurant_bookings": restaurant_bookings,
            "concert_bookings": concert_bookings,
        }
    )

def ticket(request):

    booking_id = request.GET.get("booking_id")

    booking = MovieBooking.objects.get(
        id=booking_id
    )

    return render(
        request,
        "ticket.html",
        {
            "booking": booking
        }
    )

# =========================
# EVENT DETAILS
# =========================

def event_details(request):
    event = request.GET.get('event', 'sunburn')
    return render(request, 'event_details.html', {
        'event': event
    })


# =========================
# CONCERT DETAILS
# =========================

def concert_details(request):
    concert = request.GET.get('concert', 'arijit')

    data = {
        'arijit': {
            'name': 'Arijit Singh Live',
            'location': 'Hyderabad',
            'date': '15 Aug 2026',
            'price': '₹1999 onwards',
            'image': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f',
            'description': 'Experience a magical evening with Arijit Singh.'
        },
        'rahman': {
            'name': 'A.R. Rahman Live',
            'location': 'Bangalore',
            'date': '28 Aug 2026',
            'price': '₹2499 onwards',
            'image': 'https://images.unsplash.com/photo-1501612780327-45045538702b',
            'description': 'Oscar-winning live concert.'
        },
        'diljit': {
            'name': 'Diljit Dosanjh Tour',
            'location': 'Mumbai',
            'date': '05 Sept 2026',
            'price': '₹2999 onwards',
            'image': '',
            'description': 'Punjabi music sensation live.'
        },
        'anirudh': {
            'name': 'Anirudh Live',
            'location': 'Hyderabad',
            'date': '25 Sept 2026',
            'price': '₹1999 onwards',
            'image': '',
            'description': 'High-energy musical night.'
        },
        'shreya': {
            'name': 'Shreya Ghoshal Live',
            'location': 'Chennai',
            'date': '18 Sept 2026',
            'price': '₹1499 onwards',
            'image': '',
            'description': 'Melodious live performance.'
        },
        'sunburn': {
            'name': 'Sunburn Goa 2026',
            'location': 'Goa',
            'date': '25 Dec 2026',
            'price': '₹3499 onwards',
            'image': '',
            'description': 'India’s biggest EDM festival.'
        }
    }

    item = data.get(concert, data['arijit'])

    return render(request, 'concert_details.html', {
        'item': item,
        'concert': concert
    })


# =========================
# CONCERT CHECKOUT
# =========================

def concerts_checkout(request, concert):

    concert_obj = Concert.objects.get(id=concert)

    seats = request.GET.get("seats")
    amount = request.GET.get("amount")

    request.session["concert_id"] = concert_obj.id
    request.session["concert_seats"] = seats
    request.session["concert_amount"] = amount

    return render(
        request,
        'concerts_checkout.html',
        {
            'concert': concert_obj,
            'seats': seats,
            'amount': amount
        }
    )

# =========================
# CINEMA FLOW
# =========================

def theatre_seat(request):
    movie = request.GET.get('movie', 'pushpa2')

    return render(request, 'theatre-seat.html', {
        'movie': movie
    })

from .models import Movie

def cinema_checkout(request):

    movie_id = request.GET.get("movie")

    movie = Movie.objects.get(id=movie_id)

    return render(
        request,
        "cinema-checkout.html",
        {
            "movie": movie
        }
    )

# =========================
# FAVORITES (MODEL BASED)
# =========================

def favorites(request):
    items = Favorite.objects.all().order_by('-id')

    return render(request, 'favorites.html', {
        'items': items
    })


def add_favorite(request):
    if request.method == "POST":
        Favorite.objects.create(
            name=request.POST.get("name"),
            category=request.POST.get("category"),
            location=request.POST.get("location"),
            date=request.POST.get("date"),
            time=request.POST.get("time"),
            description=request.POST.get("description"),
            image=request.POST.get("image"),
        )

    return redirect('favorites')


def remove_favorite(request, id):
    item = get_object_or_404(Favorite, id=id)
    item.delete()
    return redirect('favorites')


def favorite_detail(request, id):
    item = get_object_or_404(Favorite, id=id)

    return render(request, 'favorite_detail.html', {
        'item': item
    })


# =========================
# NOTIFICATIONS
# =========================

def notifications(request):
    notifications_list = [
        "🎟 Your IPL Final ticket is confirmed",
        "🔥 Pushpa 2 tickets are now live",
        "🎁 Get 50% off on movies today",
        "🏏 India vs Australia tickets selling fast",
        "🎤 Arijit Singh concert added near you"
    ]

    return render(request, 'notifications.html', {
        'notifications': notifications_list
    })


# =========================
# STANDUP COMEDY
# =========================

def standup_comedy(request):
    return render(request, 'standup_comedy.html')


def standup_show(request):
    return render(request, 'standup_show.html')


def standup_checkout(request):
    return render(request, 'standup_checkout.html')


# =========================
# MOVIE BOOKING FLOW FIXED
# =========================

def movie_booking(request):
    movie_id = request.GET.get('movie_id')

    if movie_id:
        return redirect(f"/theatre-seat/?movie={movie_id}")

    return redirect("/movies/")


def main_dashboard(request):
    return render(request, 'main_dashboard.html', {
        "data": DASHBOARD
    })


def search_result(request):
    query = request.GET.get('q', '')
    return render(request, 'search-result.html', {
        'query': query,
        'movies': MOVIES,
        'concerts': CONCERTS,
        'sports': SPORTS,
        'restaurants': RESTAURANTS
    })


def wishlist(request):
    items = Favorite.objects.all().order_by('-id')
    return render(request, 'wishlist.html', {
        'items': items
    })

@login_required
def settings(request):

    return render(
        request,
        "settings.html",
        {
            "user": request.user
        }
    )

def event_seat(request):
    return render(request, "event_seat.html")


def event_checkout(request):
    return render(request, "event_checkout.html")


def booking_card(request):
    booking_id = request.GET.get('booking', 'BK001')
    return render(request, 'booking_card.html', {
        'booking_id': booking_id
    })

from .models import SportsEvent

def sport_ticket(request):

    event_id = request.GET.get('event')

    event = SportsEvent.objects.get(id=event_id)

    return render(
        request,
        'sport_ticket.html',
        {
            'event': event
        }
    )

def theatre_comedy(request):
    return render(request, 'theatre_comedy.html')


def movie_details(request):
    movie = request.GET.get('movie', 'pushpa2')
    return render(request, 'movie_details.html', {
        'movie': movie
    })


def add_favorite(request):
    event = request.GET.get('event')
    ftype = request.GET.get('type')

    favorites = request.session.get('favorites', [])

    item = {"event": event, "type": ftype}

    if item not in favorites:
        favorites.append(item)

    request.session['favorites'] = favorites

    return redirect('wishlist')


def mybookings(request):
    return render(request, 'mybookings.html')


    # =========================
# STANDUP OWNER DASHBOARD
# =========================
def restaurant_dashboard(request):
    return render(request, 'restaurant_dashboard.html')
def standup_dashboard(request):
    return render(request, 'standup_dashboard.html')

def stadium_dashboard(request):
    return render(request, 'stadium_dashboard.html')

def theatre_dashboard(request):
    return render(request, 'theatre_dashboard.html')

def concerts_dashboard(request):
    return render(request, 'concerts_dashboard.html')

def create_movie_booking(request):

    if request.method == "POST":

        movie_id = request.POST.get("movie_id")

        seats = request.POST.get("seats")

        amount = request.POST.get("amount")

        movie = Movie.objects.get(id=movie_id)

        booking = MovieBooking.objects.create(
            user=request.user,
            movie=movie,
            seats=seats,
            amount=amount
        )

        return redirect(
            f"/ticket/?booking_id={booking.id}"
        )

    return redirect("movies")


from django.contrib.auth.decorators import login_required

@login_required
def create_movie_booking(request):

    if request.method == "POST":

        movie_id = request.POST.get("movie_id")
        seats = request.POST.get("seats")
        amount = request.POST.get("amount")

        movie = Movie.objects.get(id=movie_id)

        booking = MovieBooking.objects.create(
            user=request.user,
            movie=movie,
            seats=seats,
            amount=amount
        )

        return redirect(
            f"/ticket/?booking_id={booking.id}"
        )

    return redirect("movies")

from django.contrib.auth.decorators import login_required

@login_required
def create_sports_booking(request):

    print("CREATE SPORTS BOOKING CALLED")

    if request.method == "POST":

        event_id = request.POST.get("event_id")
        seats = request.POST.get("seats")
        amount = request.POST.get("amount")

        print("EVENT ID =", request.POST.get("event_id"))
        print("SEATS =", request.POST.get("seats"))
        print("AMOUNT =", request.POST.get("amount"))
        event = SportsEvent.objects.get(id=event_id)

        booking = SportsBooking.objects.create(
            user=request.user,
            event=event,
            seats=seats,
            amount=amount
        )

        return redirect(
            f"/sports-ticket-view/?booking_id={booking.id}"
        )

    return redirect("sports")

from django.shortcuts import render, redirect
from .models import RestaurantBooking, Restaurant

def payment(request):
    print("PAYMENT VIEW CALLED")

    if request.method == "POST":

        restaurant_id = request.session.get("restaurant_id")

        restaurant = Restaurant.objects.get(id=restaurant_id)
def payment(request):

    if request.method == "POST":

        restaurant_name = request.POST.get(
            "restaurant_name"
        )

        table_number = request.POST.get(
            "table_number"
        )

        RestaurantBooking.objects.create(
            user=request.user,
            restaurant_name=restaurant_name,
            booking_date=date.today(),
            booking_time=datetime.now().time(),
            guests=1,
            table_number=table_number
        )

        return redirect("my_bookings")

    amount = request.session.get("amount")

    return render(
        request,
        "card_payment.html",
        {
            "amount": amount
        }
    )

@login_required
def create_restaurant_booking(request):

    restaurant_id = request.session.get("restaurant_id")

    restaurant = Restaurant.objects.get(id=restaurant_id)

    table_number = request.GET.get("table")

    print("TABLE RECEIVED =", table_number)

    RestaurantBooking.objects.create(
        user=request.user,
        restaurant=restaurant,
        table_number=table_number
    )

    return redirect("my_bookings")

@login_required
def create_concert_booking(request):

    print("CREATE CONCERT BOOKING CALLED")

    concert_id = request.session.get("concert_id")
    seats = request.GET.get("seats")
    amount = request.GET.get("amount")

    print("CONCERT ID =", concert_id)
    print("SEATS =", seats)
    print("AMOUNT =", amount)

    concert = Concert.objects.get(id=concert_id)

    ConcertBooking.objects.create(
        user=request.user,
        concert=concert,
        seats=seats,
        amount=amount
    )

    print("BOOKING SAVED")

    return redirect("my_bookings")