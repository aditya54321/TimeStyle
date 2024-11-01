
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from TimeStyle import settings
from .models import Users,WatchDesign,DesignDetails,Cart, Payment, OrderReceipt
from .utils import *
from .validators import *
# from google_auth.views import email_script
# from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse ,HttpResponseBadRequest
from django.conf import settings
import razorpay
import json


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(email=email)
            print(user.email)
            # print(user.password)
        except Users.DoesNotExist:
            return render(request, 'signup.html', {'error': 'Invalid email'})
        if user.password == password:
            user.last_login = timezone.now()
            user.is_active=True
            request.session['user_name'] = user.first_name   # Store user data in the session user has no id 
            request.session['user_email'] = user.email
            print("login successfull")
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    else:
        return render(request, 'login.html')

@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        first = request.POST['first_name']
        last = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        # print(first,last,email,password)
        try:
            user = Users(
            first_name = first,
            last_name = last,
            email = email,
            password=password,
            is_active=True 
            )
            # print(user.first_name,user.last_name,user.email,user.password)
            user.save()
            request.session['user_name'] = user.first_name   # Store user data in the session user has no id 
            request.session['user_email'] = user.email
            # user = Users.objects.create_user(email=email, password=password)
            # login(request, user)
            login_view(request)
            return redirect('home')
        except:
            return render(request, 'signup.html', {'error': 'An error occurred'})
    else:
        return render(request, 'signup.html')

    




class HomeView(View):
    def get(self, request,design_id = None):
        if design_id :
            try:
                design_details = get_object_or_redirect(DesignDetails, watch_design_id=design_id)
                return render(request, 'design_detail.html', {'design_details': design_details})
            except: 
                return redirect('home')
                # return render(request, 'home.html', {'error': 'This item is currently unavailable'})
        else:
            designs = WatchDesign.objects.all()
            return render(request, 'home.html', {'designs': designs})
        



def cart(request):
    user_name = request.session.get('user_name')
    user_email = request.session.get('user_email')
    cart_items = Cart.objects.filter(user__email=user_email, in_cart=True)
    context = {
        'cart_items': cart_items,
        'user_name' : user_name,
        'user_email' :user_email
    }
    return render(request, 'cart.html', context)


@csrf_protect
def addtocart(request, design_id):
    user_email = request.session.get('user_email')
    euser = get_object_or_redirect(Users, email=user_email)
    if euser:
        design = WatchDesign.objects.get(pk=design_id)
        # design_details = DesignDetails.objects.get(watch_design=design)
        design_details = get_object_or_redirect(DesignDetails,watch_design=design)
        existing_order = Cart.objects.filter(user__email=user_email, design=design_id, in_cart=True).first()
        print (euser.first_name,euser.email,design.id)
        if existing_order and request.method == 'GET':
            existing_order.quantity += 1
            existing_order.save()
            print(existing_order.user, existing_order.order_date,"\n order is already in cart updated quantity")
        elif  request.method == 'POST' :
            quantity = request.POST.get('quantity')
            print(quantity)
            existing_order.quantity = quantity
            existing_order.save()
        else:
            # print("order not found \n")
            Cart.objects.create(user=euser, design=design_details, in_cart=True, quantity = 1)
        return redirect('cart')
    else:
        return redirect('login')
    

    
@csrf_protect
def decrement_cart(request, design_id):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        euser = Users.objects.get(email=user_email)
        if euser:
            design = WatchDesign.objects.get(pk=design_id)
            print(design.name)
            existing_order = Cart.objects.filter(user__email=user_email, design=design_id, in_cart=True).first()
            if existing_order:
                if existing_order.quantity > 1:  # Ensure quantity doesn't go below 1
                    existing_order.quantity -= 1
                    existing_order.save()
            return redirect('cart')
    else:
        return redirect('login')

@csrf_protect
def remove_from_cart(request, design_id):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        euser = Users.objects.get(email=user_email)
        if euser :
            design = WatchDesign.objects.get(pk=design_id)
            print(design.name)
            existing_order = Cart.objects.filter(user__email=user_email, design=design_id, in_cart=True).first()
            if existing_order:
                existing_order.delete() 
            return redirect('cart')
    else:
        return redirect('login')






































def initiate_payment(request):
    if request.method == "POST":
        amount = float(request.POST["amount"])*100
        amount = int(amount)   # Amount in paise
        # item_id = request.POST["item_id"]
        # item_quantity = request.POST["quantity"]
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        # data for processing checkout
        payment_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "unique_value_used_AS_receipt",
            "notes": {
                "email": "user_email@example.com",
                "item_id" : "item_id",
                "item_name" : "item_name",
                "quantity" : "quantity"
            },
            "partial_payment" : False,
        }
        # order id genterated 
        order = client.order.create(data=payment_data)
        print(order)
        # Include key, name, description, and image in the JSON response
        response_data = {
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            # "payment_id": order["payment_id"],
            # "order_id" : order["order_id"],
            # "signature" : order["signature"],
            "key": settings.RAZORPAY_API_KEY,
            "name": "Your Company Name",
            "description": "Payment for Your Product",
            "image": "https://yourwebsite.com/logo.png",  # Replace with your logo URL
        }
        # return render(request, 'payment_success.html', {'response': response_data})
        return JsonResponse(response_data)
    
    return render(request, "payment.html")


def payment_success(request):
    return render(request, "payment_success.html")


# @csrf_protect
# def payment_success(request):
#     if request.method == "POST":
#         razorpay_payment_id = request.POST.get('razorpay_payment_id')
#         razorpay_order_id = request.POST.get('razorpay_order_id')
#         razorpay_signature = request.POST.get('razorpay_signature')

#         # Verify the payment signature using Razorpay's utility functions (optional but recommended)
#         try:
#             client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': razorpay_payment_id,
#                 'razorpay_signature': razorpay_signature
#             }
#             result = client.utility.verify_payment_signature(params_dict)
#             if result:
#                 # Payment is successful and verified
#                 # Handle the business logic here (e.g., update order status, send confirmation email)
#                 # return JsonResponse({'status': 'success'})
#                 return render(request, "payment_success.html")
#             else:
#                 return HttpResponseBadRequest("Invalid payment signature")
#         except:
#             return HttpResponseBadRequest("Payment verification failed")

def payment_failed(request):
    return render(request, "payment_failed.html")




# @csrf_exempt
# def create_order(request):

#     if request.method == 'POST':
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
#         # user = request.user
#         user_email = request.session.get('user_email')
#         user = get_object_or_redirect(Users, email = user_email)
#         item_id = request.POST.get('item_id', None)
#         quantity = int(request.POST.get('quantity', 1))
#         if item_id is not None:
#             item = DesignDetails.objects.get(id=item_id)
#             amount = item.price * quantity  # The amount is now based on the quantity.
#         else:
#             #adding logic .....
#             amount = 0  

#         cart_details = Cart.objects.get(user = user, design = item)
#         print(cart_details.status)

#         # cart_details.save()
#         # Create a new order in Razorpay.
#         data = {
#             'amount': int(amount * 100),  # The amount must be in paisa.
#             'currency': 'INR',
#             'receipt': str(item_id), #cart_details.design.name,
#             'payment_capture': '1'
#         }
#         razorpay_order = client.order.create(data=data)

# response that we are getting is  = {'amount': 40000, 'amount_due': 40000, 'amount_paid': 0,
#  'attempts': 0,'created_at': 1729783418, 'currency': 'INR', 
# 'entity': 'order', 'id': 'order_PCvILKTnXfQfV3',
#  'notes': {'email': 'user_email@example.com', 'item': 'item'},'offer_id': None,
# 'receipt': 'unique_value_use_AS_receipt', 'status': 'created'}


#         # Store the Razorpay order ID in your database.
#         payment = Payment.objects.create(user=user, order=cart_details, razorpay_id=razorpay_order['id'], amount=amount)
        
#         order_receipt = OrderReceipt.objects.create(
#             cart=cart_details,
#             payment=payment,
#             total_quantity=quantity,
#             total_amount = amount
#             )
#         order_receipt.save()
#         cart_details  = Cart.objects.update(
#             is_manufactured = True,
#             status = 'Shipped'
#             # quantity need to be reduce and if single item then it must set in_cart = false
#             )

#         return JsonResponse({'razorpay_order_id': razorpay_order['id']}, safe=True)
#     else:
#         return redirect('home')







def purchase_result(request):
    if request.method == 'GET':
        payment_id = request.GET.get('payment_id', None)
        if payment_id is not None:
            payment = Payment.objects.get(payment_id=payment_id)
            if payment.status == 'Successful':
                # The payment was successful.
                # Generate an invoice and save it in the OrderReceipt model.
                receipt = OrderReceipt.objects.create(order=payment.order, payment=payment, total_quantity=payment.order.quantity, total_amount=payment.amount)
                return render(request, 'purchase_result.html', {'receipt': receipt})
            else:
                # The payment failed.
                return render(request, 'purchase_result.html', {'error': 'The payment failed.'})
        else:
            return redirect('home')
    else:
        return redirect('home')







@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['event'] == 'payment.authorized':
            # The payment was successful.
            payment_id = data['payload']['payment']['entity']['id']
            payment = Payment.objects.get(razorpay_id=payment_id)
            payment.status = 'Successful'
            payment.save()
        elif data['event'] == 'payment.failed':
            # The payment failed.
            payment_id = data['payload']['payment']['entity']['id']
            payment = Payment.objects.get(razorpay_id=payment_id)
            payment.status = 'Failed'
            payment.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)



