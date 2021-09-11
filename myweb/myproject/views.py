import json
import razorpay
from math import ceil
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Product, Contact, Order, OrderUpdate, Register

MERCHANT_KEY = 're4IKy2WlZxGssBe';

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))


# Create your views here.
def front(request):
    return render(request, 'front.html')


def index(request):
    return render(request, 'index.html')


def comingsoon(request):
    return render(request, 'comingsoon.html')


def paymentfailed(request):
    return render(request, 'paymentfailed.html')


def paymentsuccess(request):
    return render(request, 'paymentsuccess.html')


def products(request):
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'products.html', params)


def products2(request):
    allProds = []
    catProds = Product.objects.values('subcategory', 'id').order_by('sequence_id')
    cats = {item['subcategory'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat).order_by('sequence_id')
        n = len(prod)
        nSlides = n // 3 + ceil((n / 3) - (n // 3))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'products2.html', params)


def desserts(request):
    allProds = []
    catProds = Product.objects.values('subcategory', 'id').filter(category='Desserts').order_by('sequence_id')
    cats = {item['subcategory'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat).order_by('sequence_id')
        n = len(prod)
        nSlides = n // 3 + ceil((n / 3) - (n // 3))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'desserts.html', params)


def bestseller(request):
    allProds = []
    catProds = Product.objects.values('subcategory', 'id').filter(category='Best Seller').order_by('sequence_id')
    cats = {item['subcategory'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat).order_by('sequence_id')
        n = len(prod)
        nSlides = n // 3 + ceil((n / 3) - (n // 3))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'bestseller.html', params)


def cakes(request):
    allProds = []
    catProds = Product.objects.values('subcategory', 'id').filter(category='Cakes').order_by('sequence_id')
    cats = {item['subcategory'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat).order_by('sequence_id')
        n = len(prod)
        nSlides = n // 3 + ceil((n / 3) - (n // 3))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'cakes.html', params)


def cookiesandbrownies(request):
    allProds = []
    catProds = Product.objects.values('subcategory', 'id').filter(category='Cookies And Brownies').order_by(
        'sequence_id')
    cats = {item['subcategory'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat).order_by('sequence_id')
        n = len(prod)
        nSlides = n // 3 + ceil((n / 3) - (n // 3))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'cookiesandbrownies.html', params)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        res = Register(username=username, password=password)
        if len(res) > 0:
            return render(request, 'front.html', {'output': "Login Successful"})
        else:
            return render(request, 'login.html', {'output': "Login Failed!!!"})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        register = Register(username=username, email=email, password=password, phone=phone)
        register.save()
    return render(request, 'login.html', {'output': "Register Successfully"})


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'contact.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'tracker.html')


def searchMatch(query, item):
    # return true only if query matches the item
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'search.html', params)


def productView(request, myid):
    # fetch the product using id
    product = Product.objects.filter(id=myid)
    return render(request, 'prodView.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        add1 = request.POST.get('add1', '')
        add2 = request.POST.get('add2', '')
        city = request.POST.get('city', '')
        area = request.POST.get('area', '')
        pincode = request.POST.get('pincode', '')
        order = Order(items_json=items_json, amount=amount, fname=fname, lname=lname, email=email,
                      phone=phone, add1=add1,
                      add2=add2, city=city, area=area, pincode=pincode)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="the Order has been placed Successfully...")
        update.save()

        # razorpay

        currency = 'INR'
        amount = 20000  # Rs. 200

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture=1))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'https://eneqd3r9zrjok.x.pipedream.net/'

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZORPAY_API_KEY
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url

    return render(request, 'checkout.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:

                    # capture the payment
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful capture of payment
                    return render(request, 'paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
