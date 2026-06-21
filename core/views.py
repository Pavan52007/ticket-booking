from django.shortcuts import render, redirect, get_object_or_404
from .models import Favorite
from .data import MOVIES, CONCERTS, RESTAURANTS, SPORTS, OFFERS, DASHBOARD


# =========================
# BASIC PAGES
# =========================

def home(request):
    return render(request, 'home.html')

def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")
        promoter_type = request.POST.get("promoter_type")

        print(username)
        print(password)
        print(role)
        print(promoter_type)

        if role == "customer":
            return redirect("dashboard")

        elif role == "admin":
            return redirect("admin_dashboard")

        elif role == "promoter":

            if promoter_type == "standup_comedy_owner":
                return redirect("standup_dashboard")

            elif promoter_type == "theatre_owner":
                return redirect("dashboard")

            elif promoter_type == "restaurant_owner":
                return redirect("restaurant_dashboard")

            elif promoter_type == "stadium_owner":
                return redirect("dashboard")

            elif promoter_type == "music_concert_owner":
                return redirect("dashboard")

    return render(request, "login.html")

# ✅ FIXED: now saves user data in session
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        request.session['user'] = {
            "username": username,
            "email": email,
            "password": password
        }

        return redirect('dashboard')

    return render(request, 'register.html')


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


def events(request):
    return render(request, 'events.html')


def event_details(request):
    return render(request, 'event_details.html')


def movies(request):
    return render(request, 'movies.html', {
        "movies": MOVIES
    })


def concerts(request):
    return render(request, 'concerts.html', {
        "concerts": CONCERTS
    })


def sports(request):
    return render(request, 'sports.html', {
        "sports": SPORTS
    })


def restaurants(request):
    return render(request, 'restaurants.html', {
        "restaurants": RESTAURANTS
    })


def offers(request):
    return render(request, 'offers.html', {
        "offers": OFFERS
    })


# =========================
# BOOKINGS
# =========================

def table_booking(request):
    restaurant = request.GET.get('restaurant', 'Restaurant')
    return render(request, 'table-booking.html', {
        'restaurant': restaurant
    })


def booking(request):
    restaurant = request.GET.get('restaurant', 'Restaurant')

    return render(request, 'booking_card.html', {
        'restaurant': restaurant
    })


def sports_checkout(request):
    event = request.GET.get('event', 'cskmi')
    return render(request, 'sports-checkout.html', {
        'event': event
    })


def my_bookings(request):
    return render(request, 'mybookings.html')


def ticket(request):
    booking = request.GET.get('booking', 'SUN001')
    return render(request, 'ticket.html', {
        'booking': booking
    })


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
    return render(request, 'concerts_checkout.html', {
        'concert': concert
    })


# =========================
# CINEMA FLOW
# =========================

def theatre_seat(request):
    movie = request.GET.get('movie', 'pushpa2')

    return render(request, 'theatre-seat.html', {
        'movie': movie
    })


def cinema_checkout(request):
    movie = request.GET.get('movie', 'pushpa2')
    seats = request.GET.get('seats', '')

    return render(request, 'cinema-checkout.html', {
        'movie': movie,
        'seats': seats
    })


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
    movie = request.GET.get('movie', 'pushpa2')
    return redirect(f"/theatre-seat/?movie={movie}")


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


def settings_page(request):
    user = request.session.get('user')

    return render(request, 'settings.html', {
        'user': user
    })

def event_seat(request):
    return render(request, "event_seat.html")


def event_checkout(request):
    return render(request, "event_checkout.html")


def booking_card(request):
    booking_id = request.GET.get('booking', 'BK001')
    return render(request, 'booking_card.html', {
        'booking_id': booking_id
    })


def sport_ticket(request):
    event = request.GET.get('event', 'cskmi')
    return render(request, 'sport_ticket.html', {
        'event': event
    })


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
