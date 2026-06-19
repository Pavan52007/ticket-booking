from django.template.loader import get_template
from xhtml2pdf import pisa
import qrcode
from reportlab.lib.utils import ImageReader
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Booking, Seat
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import RestaurantBooking, RestaurantTable
from datetime import date, datetime

def home(request):
    return render(request, 'home.html')


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
            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid Username or Password"
            }
        )

    return render(request, "login.html")


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(
                request,
                "register.html",
                {"error": "Passwords do not match"}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "register.html",
                {"error": "Username already exists"}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "register.html")


def dashboard(request):
    return render(request, 'main_dashboard.html')


def events(request):
    return render(request, 'events.html')


def movies(request):
    return render(request, 'movies.html')


def sports(request):
    return render(request, 'sports.html')


def restaurants(request):
    return render(request, 'restaurants.html')

def table_booking(request):

    if request.method == "POST":
        print("TABLE BOOKING POST RECEIVED")
        print(request.POST)
        print("TABLE =", request.POST.get("table_number"))
        booking_date = date.today()
        booking_time = datetime.now().time()
        guests = 1

        restaurant_name = request.POST.get("restaurant_name")
        table_number = request.POST.get("table_number")

        booking = RestaurantBooking.objects.create(
            user=request.user,
            restaurant_name=restaurant_name,
            booking_date=booking_date,
            booking_time=booking_time,
            guests=guests,
            table_number=table_number
        )

        table = RestaurantTable.objects.filter(
            restaurant_name=restaurant_name,
            table_number=table_number,
            is_booked=False
        ).first()

        if table:
            table.is_booked = True
            table.booking = booking
            table.save()

        return redirect("my_bookings")

    return render(request, "table-booking.html")


def booking(request):
    restaurant = request.GET.get('restaurant')

    return render(
        request,
        'book_ticket.html',
        {
            'restaurant': restaurant
        }
    )


# SPORTS CHECKOUT PAGE
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
# MY BOOKINGS PAGE
from .models import Booking, Seat


def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    )

    for booking in bookings:
        allocated = Seat.objects.filter(
            booking=booking
        )

        booking.allocated_seats = ", ".join(
            [seat.seat_number for seat in allocated]
        )

    restaurant_bookings = RestaurantBooking.objects.filter(
        user=request.user
    )

    return render(
        request,
        "my_bookings.html",
        {
            "bookings": bookings,
            "restaurant_bookings": restaurant_bookings
        }
    )
# TICKET PAGE
from .models import Booking

def ticket(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    allocated = Seat.objects.filter(
        booking=booking
    )

    seat_numbers = ", ".join(
        [seat.seat_number for seat in allocated]
    )

    return render(
        request,
        "ticket.html",
        {
            "booking": booking,
            "seat_numbers": seat_numbers
        }
    )

# OFFERS & COUPONS PAGE
def offers(request):
    return render(request, 'offers.html')


def event_details(request):
    event = request.GET.get('event', 'sunburn')

    data = {

        'standup': {
            'title': 'Standup Comedy',
            'date': '12 June 2026',
            'time': '8:00 PM',
            'venue': 'Hyderabad',
            'price': '499',
            'image': 'https://images.pexels.com/photos/713149/pexels-photo-713149.jpeg',
            'description': 'Enjoy a night full of laughter with top comedians.'
        },

        'cricket': {
            'title': 'Cricket Match',
            'date': '12 June 2026',
            'time': '7:30 PM',
            'venue': 'Hyderabad Stadium',
            'price': '799',
            'image': 'https://images.pexels.com/photos/1661950/pexels-photo-1661950.jpeg',
            'description': 'Watch an exciting live cricket match.'
        },

        'food': {
            'title': 'Food Festival',
            'date': '18 June 2026',
            'time': '5:00 PM',
            'venue': 'Hyderabad',
            'price': '299',
            'image': 'https://images.pexels.com/photos/315191/pexels-photo-315191.jpeg',
            'description': 'Taste delicious dishes from around the world.'
        },

        'pushpa2': {
            'title': 'Pushpa 2',
            'date': '2024 Release',
            'time': '6:00 PM',
            'venue': 'PVR Cinemas',
            'price': '350',
            'image': 'https://m.media-amazon.com/images/M/MV5BNDM3N2UzM2UtMjEwMC00NGUzLThmMmQtNGMyM2VmMDA0ZWEwXkEyXkFqcGc@._V1_.jpg',
            'description': 'Watch the blockbuster movie Pushpa 2.'
        },

        'ipl': {
            'title': 'IPL Finals',
            'date': '25 June 2026',
            'time': '7:00 PM',
            'venue': 'Ahmedabad Stadium',
            'price': '1499',
            'image': 'https://images.pexels.com/photos/1661950/pexels-photo-1661950.jpeg',
            'description': 'Experience the IPL Final live.'
        },

        'paradise': {
            'title': 'Paradise Biryani',
            'date': 'Open Daily',
            'time': '11:00 AM - 11:00 PM',
            'venue': 'Hyderabad',
            'price': '499',
            'image': 'https://images.pexels.com/photos/67468/pexels-photo-67468.jpeg',
            'description': 'Enjoy authentic Hyderabadi biryani.'
        },

        'bbq': {
            'title': 'Barbeque Nation',
            'date': 'Open Daily',
            'time': '12:00 PM - 11:00 PM',
            'venue': 'Hyderabad',
            'price': '799',
            'image': 'https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg',
            'description': 'Unlimited buffet with live grills.'
        },

        'pizzahut': {
            'title': 'Pizza Hut',
            'date': 'Open Daily',
            'time': '11:00 AM - 11:00 PM',
            'venue': 'Hyderabad',
            'price': '299',
            'image': 'https://images.pexels.com/photos/941861/pexels-photo-941861.jpeg',
            'description': 'Fresh pizzas and Italian food.'
        },

        'sunburn': {
            'title': 'Sunburn Festival',
            'date': '10 July 2026',
            'time': '7:00 PM',
            'venue': 'Hyderabad',
            'price': '999',
            'image': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7',
            'description': 'India’s biggest EDM festival.'
        }
    }

    return render(
        request,
        'event_details.html',
        data.get(event, data['sunburn'])
    )
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

from django.http import HttpResponse
from reportlab.pdfgen import canvas

def download_ticket(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        f'attachment; filename="ticket_{booking.ticket_id}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(100, 800, "ZENITH EVENTS TICKET")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 760, f"Ticket ID: {booking.ticket_id}")
    pdf.drawString(100, 730, f"Event: {booking.event_name}")
    pdf.drawString(100, 700, f"Seats: {booking.seats}")
    pdf.drawString(100, 670, f"Amount: Rs.{booking.amount}")
    pdf.drawString(100, 640, f"Status: {booking.status}")
    pdf.drawString(100, 610, f"User: {booking.user.username}")

    pdf.save()

    return response
def restaurant_ticket(request, booking_id):

    booking = RestaurantBooking.objects.get(
        id=booking_id
    )

    return render(
        request,
        "restaurant_ticket.html",
        {
            "booking": booking
        }
    )