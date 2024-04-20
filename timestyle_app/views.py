from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Users,WatchDesign,DesignDetails,Order
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(email=email)
            print(user.email)
            print(user.password)
        except Users.DoesNotExist:
            return render(request, 'signup.html', {'error': 'Invalid email'})
        if user.password == password:
            user.last_login = timezone.now()
            user.is_active=True
            login(request, user)
            request.session['user_name'] = user.first_name   # Store user data in the session user has no id 
            request.session['user_email'] = user.email
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid password'})
    else:
        return render(request, 'login.html')

@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        first = request.POST['first_name']
        last = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Users()
            user.first_name=first,
            user.last_name = last,
            user.email = email,
            user.password=password,
            # print(user.first_name,user.last_name,user.email,user.password)
            user.save()
            user.is_active=True 
            # user = Users.objects.create_user(email=email, password=password)
            login(request, user)
            return redirect('home')
        except:
            return render(request, 'signup.html', {'error': 'An error occurred'})
    else:
        return render(request, 'signup.html')

    
def home(request):
    designs = WatchDesign.objects.all()
    return render(request, 'home.html', {'designs': designs})


def details_view(request, design_id):
    try:
        design_details = get_object_or_404(DesignDetails, watch_design_id=design_id)
        return render(request, 'design_detail.html', {'design_details': design_details})
    except: 
        return redirect('home')
        # return render(request, 'home.html', {'error': 'This item is currently unavailable'})


def cart(request):
    # user_name = request.session.get('user_name')
    user_email = request.session.get('user_email')
    cart_items = Order.objects.filter(user__email=user_email, in_cart=True)
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)

def addtocart(request, design_id):
    user_email = request.session.get('user_email')
    euser = Users.objects.get(email=user_email)
    if euser:
        design = WatchDesign.objects.get(pk=design_id)
        existing_order = Order.objects.filter(user__email=user_email, design=design_id, in_cart=True).first()
        print (euser.first_name,euser.email,design.id)
        if existing_order :
            existing_order.quantity += 1
            existing_order.save()
            print(existing_order.user, existing_order.order_date,"\n order is already in cart updated quantity")
        else:
            # print("order not found \n")
            Order.objects.create(user=euser, design=design, in_cart=True)
        return redirect('cart')
    else:
        return redirect('login')



































# def addtocart(request, design_id):
#     user_name = request.session.get('user_name')
#     user_email = request.session.get('user_email')

#     # Print user details      and user_name
#     if user_email :
#         print(f"s_mail: {user_email}")
#         print(f"s_name: {user_name}")
#     else:
#         return redirect('login')
#     return redirect('signup')

    # Access the details of the currently authenticated user
    # authenticated_user = request.user
    # if authenticated_user.is_authenticated:
            # print(f"User ID: {authenticated_user.id}")
            # print(f"Username: {authenticated_user.username}")
            # print(f"Email: {authenticated_user.email}")