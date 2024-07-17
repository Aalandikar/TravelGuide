from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Destination, ThingToExplore, MustVisitPlace
from .forms import BookingForm, SearchForm, UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User

def home(request):
        return render(request, 'travel/home.html')


def destination(request):
    
    destinations = Destination.objects.all()
    return render(request, 'travel/destination.html', {'destinations': destinations})

def search(request):
    query = request.GET.get('query')
    if query:
        results = Destination.objects.filter(name__icontains=query)  # Adjust the filter as needed
    else:
        results = Destination.objects.none()
    return render(request, 'travel/search_results.html', {'results': results, 'query': query})

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    print(f"Destination: {destination.name}")  # Debugging statement
    booking_form = BookingForm()

    context = {
        'destination': destination,
        'booking_form': booking_form
    }

    return render(request, 'destination_detail.html', context)

def calculate_amount(destination, num_adults, num_children):
    return (destination.price_adult * num_adults) + (destination.price_child * num_children)

def book_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.destination = destination
            # Calculate amount based on destination prices and number of persons
            price_adult = destination.price_adult
            price_child = destination.price_child
            num_adults = booking_form.cleaned_data['num_adults']
            num_children = booking_form.cleaned_data['num_children']
            booking.amount = calculate_amount(destination, booking.num_adults, booking.num_children)
            print(f"Calculated Amount: {booking.amount}") 
            booking.save()

            # Initiate Razorpay payment
            client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))
            amount_in_paise = int(booking.amount * 100)  # Razorpay accepts amount in paise (1 INR = 100 paise)
            payment_data = {
                'amount': amount_in_paise,
                'currency': 'INR',  # Adjust as per your currency
                'receipt': f'booking_{booking.id}',
                'payment_capture': 1  # Auto capture payment after order creation
            }
            razorpay_order = client.order.create(data=payment_data)

            return render(request, 'travel/booking_confirmed.html', {
                'booking': booking,
                'payment': razorpay_order,
                'razorpay_key_id': settings.RAZORPAY_TEST_KEY_ID
            })
    else:
        booking_form = BookingForm(initial={'destination': destination})

    return render(request, 'travel/book_destination.html', {
        'destination': destination,
        'booking_form': booking_form,
    })

def things_to_explore(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    things_to_explore = ThingToExplore.objects.filter(destination=destination)
    return render(request, 'travel/things_to_explore.html', {
        'destination': destination,
        'things_to_explore': things_to_explore,
    })

def must_visit_places(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    must_visit_places = MustVisitPlace.objects.filter(destination=destination)
    return render(request, 'travel/must_visit_places.html', {
        'destination': destination,
        'must_visit_places': must_visit_places,
    })
  
def register(request):
    if request.method=='POST':
        uname=request.POST['uname'] #""
        uemail=request.POST['uemail']
        upass=request.POST['upass'] #""
        ucpass=request.POST['ucpass'] #""
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields can not be empty"
        elif upass!=ucpass:
            context['errmsg']="Password & confirm password did not matched"
        else:
            try:    
                u=User.objects.create(password=upass,username=uname,email=uemail)  #colname=value
                u.set_password(upass)
                u.save()
                context['success']="User Created Successfully"
            except Exception:
                context['errmsg']="User with the same name already Exit!!"
        return render(request,'register.html',context)
        #return HttpResponse("Data is fetched "+uname)
    else:
        return render(request,'register.html')  #GET
    
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('destination')
            else : 
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'travel/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')



def payment_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'payment_confirmation.html', {'booking': booking})
    

def send_confirmation_email(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    subject = 'Booking Confirmation'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [booking.user.email]

    text_content = render_to_string('booking_confirmation_email.txt', {'booking': booking})
    html_content = render_to_string('booking_confirmation_email.html', {'booking': booking})
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return render(request, 'travel/email_sent.html', {'booking': booking})
    #return HttpResponse("Email sent successfully!")


