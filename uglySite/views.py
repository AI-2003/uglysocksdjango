from django import forms
from django.shortcuts import render, redirect
from .forms import SearchForm, ReviewForm, CheckoutForm, CheckoutForm1, CartForm, CustomImagesForm, CustomImagesURLForm
from .models import Product, ProductImage, Review, Order, Address, StripeReceipt, CustomImage
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import uuid
from uglysocks import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
import re
from io import BytesIO
from django.core.files import File
import base64
from PIL import Image

stripe.api_key = "sk_test_0q9BNL8DVS1X1xS1u46YyA1M00RmBsmehw"

# Create your views here.

def loadCustom(request, ID):
    try:
        image = CustomImage.objects.get(uuid=uuid.UUID(ID))
        return HttpResponse(image.front.url,content_type="application/str")
    except:
        return HttpResponse("",content_type="application/str")




def landing(request):

    
    
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())


    context = {
        "form": SearchForm(),
    }
    return render(request, 'landing.html', context)


def category(request, categoryName):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())

    
    productList = Product.objects.filter(categories__categories__contains=categoryName)
    listLength = productList.count()

    context = {
        "form": SearchForm(),
        "productList": productList,
        "searchName": categoryName,
        "listLength": listLength,
        "notFound": "Ups! Parece que no hay ninguna categoría llamada ("+categoryName+")",

    }
    return render(request, 'search.html', context)

def make_image(image, name, size=(1000,4500)):
    im = Image.open(BytesIO(image))
    im.resize(size, Image.ANTIALIAS)
    thumb_io = BytesIO()
    im.save(thumb_io, "PNG", quality=100)
    thumbnail = File(thumb_io, name=name)
    return thumbnail

def product(request, identifier):

    product = Product.objects.get(pk=identifier)
    categoryName = product.categories["categories"][0]
    gallery = ProductImage.objects.filter(product=product)
    relProd = Product.objects.filter(categories__categories__contains=categoryName).exclude(pk=product.id)[:4]
    reviews = Review.objects.filter(product=product).filter(published=True)
    images=""


 
    try:
        objCheck = CustomImage.objects.get(uuid=settings.IMG_UUID)
        if objCheck != None:
            settings.IMG_UUID = uuid.uuid4()
    except: 
        print("No obj found!")
        print("UUID: ", settings.IMG_UUID)

    imguuid = settings.IMG_UUID

    ratSum = 0.0
    for r in reviews:
        ratSum+=float(r.rating)

    numOfReviews=reviews.count()
    product.reviews=numOfReviews
    if numOfReviews > 0:
        product.rating=ratSum/numOfReviews
    else:
        product.rating=0.0
    product.save()

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())

        form2 = ReviewForm(request.POST)
        if form2.is_valid():
            review = Review(
                product=product,
                reviewer=request.POST.__getitem__("reviewer"),
                review=request.POST.__getitem__("review"),
                email=request.POST.__getitem__("email"),
                rating=abs(float(request.POST.__getitem__("rating")))
            )
            review.save()
            
            return redirect("product", identifier=identifier)
        


        form4 = CustomImagesForm(request.POST)
        if form4.is_valid():

            #try:
                if "uuid" in request.POST:
                    if str(imguuid) == request.POST.__getitem__("uuid"):
                        if "fronturl" in request.POST and "backurl" in request.POST:
                            if request.POST.__getitem__("fronturl")!="" and request.POST.__getitem__("backurl")!="":
                                frontstr = re.search(r'base64,(.*)', request.POST.__getitem__("fronturl")).group(1)
                                backstr = re.search(r'base64,(.*)', request.POST.__getitem__("backurl")).group(1)
                                img = CustomImage(
                                    uuid=imguuid,
                                    front=make_image(base64.b64decode(frontstr), str(imguuid)+".png", size=(1000,4500)),
                                    back=make_image(base64.b64decode(backstr), str(imguuid)+".png", size=(1000,4500)),
                                )
                                img.save()
                                settings.IMG_UUID = uuid.uuid4()
                                return HttpResponse(
                                    json.dumps({"uuid": str(img.uuid), "newuuid":   str(settings.IMG_UUID), "fronturl": str(img.front.url), "success": "True",}),
                                    content_type="application/json"
                                )
                            elif request.POST.__getitem__("fronturl")!="":
                                frontstr = re.search(r'base64,(.*)', request.POST.__getitem__("fronturl")).group(1)
                                img = CustomImage(
                                    uuid=imguuid,
                                    front=make_image(base64.b64decode(frontstr), str(imguuid)+".png", size=(1000,4500)),
                                )
                                img.save()
                                settings.IMG_UUID = uuid.uuid4()
                                return HttpResponse(
                                    json.dumps({"uuid": str(img.uuid), "newuuid":   str(settings.IMG_UUID), "fronturl": str(img.front.url), "success": "True",}),
                                    content_type="application/json"
                                )
                            elif request.POST.__getitem__("backurl")!="":
                                backstr = re.search(r'base64,(.*)', request.POST.__getitem__("backurl")).group(1)
                                img = CustomImage(
                                    uuid=imguuid,
                                    back=make_image(base64.b64decode(backstr), str(imguuid)+".png", size=(1000,4500)),
                                )
                                img.save()
                                settings.IMG_UUID = uuid.uuid4()
                                return HttpResponse(
                                    json.dumps({"uuid": str(img.uuid), "newuuid":   str(settings.IMG_UUID), "fronturl": str(img.front.url), "success": "True",}),
                                    content_type="application/json"
                                )

                        elif "fronturl" not in request.POST and "backurl" in request.POST:
                            if request.POST.__getitem__("backurl")!="":
                                backstr = re.search(r'base64,(.*)', request.POST.__getitem__("backurl")).group(1)
                                img = CustomImage(
                                    uuid=imguuid,
                                    back=make_image(base64.b64decode(backstr), str(imguuid)+".png", size=(1000,4500)),
                                )
                                img.save()
                                settings.IMG_UUID = uuid.uuid4()
                                return HttpResponse(
                                    json.dumps({"uuid": str(img.uuid), "newuuid":   str(settings.IMG_UUID), "fronturl": str(img.front.url), "success": "True",}),
                                    content_type="application/json"
                                )
                                
                        elif "fronturl" in request.POST and "backurl" not in request.POST:
                            
                            if request.POST.__getitem__("fronturl")!="":
                                frontstr = re.search(r'base64,(.*)', request.POST.__getitem__("fronturl")).group(1)
                                img = CustomImage(
                                    uuid=imguuid,
                                    front=make_image(base64.b64decode(frontstr), str(imguuid)+".png", size=(1000,4500)),
                                )
                                img.save()
                                settings.IMG_UUID = uuid.uuid4()
                                return HttpResponse(
                                    json.dumps({"uuid": str(img.uuid), "newuuid":   str(settings.IMG_UUID), "fronturl": str(img.front.url), "success": "True",}),
                                    content_type="application/json"
                                )                 
                    else:
                        print("MMM That's not the uuid")
                        return redirect("/error/", errorMsg="Algo salió mal.")
            #except:
                #return redirect("/error/", "Algo salió mal.")

    
    context = {
        "form": SearchForm(),
        "product": product,
        "gallery": gallery,
        "reviewForm": ReviewForm(),
        "numOfRev": numOfReviews,
        "reviews": reviews,
        "relProd": relProd,
        "customProduct": product.custom,
        "cartForm": CartForm(),
        "customImages": images,
        "CustomImagesURLForm": CustomImagesURLForm(),
        "imagesForm": CustomImagesForm(),
        "uuid": imguuid,
    }
    return render(request, 'product.html', context)

def search(request, text):

    productList = Product.objects.filter(name__contains=text.lower())

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())

    listLength = productList.count()

    context = {
        "searchName": "Resultados para ("+text+"):",
        "form": SearchForm(),
        "productList": productList,
        "listLength": listLength,
        "notFound": "Ups! Parece que no hay resultados para ("+text+")",
    }
    return render(request, 'search.html', context)

def policy(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())

    context={
        "form": SearchForm(),
    }
    return render(request, 'policy.html', context)

def extendedPolicy(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())

    context={
        "form": SearchForm(),
    }
    return render(request, 'extendedPolicy.html', context)

def succeed (request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())


    descrip="Un correo ya fue enviado con los detalles de tu compra. Por favor mantente atento."

    context= {
        "message": "Wuju!",
        "descrip": descrip,
        "form": SearchForm()
    }
    return render(request, 'message.html', context)

def error(request, errorMsg=" "):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())

    context={
        "message": "Ups! "+errorMsg,
        "form": SearchForm()
    }
    return render(request, "message.html", context)


def loading(request):


    context = {}
    return render(request, "loading.html", context)

def checkout(request):

    cartHas=True

    try:
        objCheck = Order.objects.get(id=settings.ORDER_UUID)
        if objCheck != None:
            settings.ORDER_UUID = uuid.uuid4()
    except: 
        print("No obj found!")

    myUUID = settings.ORDER_UUID
    canUpdate = True

    order = {
        "totalPrice": 0,
    }

    cookCart = json.loads(request.COOKIES.get("cart", "{}"))
    
    customImages = {}

    for key in cookCart:
        prod = Product.objects.get(pk=key)    
        numOfProd = 0
        custom = cookCart[key]["custom"]=="True"
        order[key] = {
            "totalProd": 0,
            "totalPrice": 0,
            "name": prod.name,
            "variations": {},
            "custom": custom,
        }

        if not custom:
            for sub in cookCart[key]:
                if sub!="src" and sub!="price" and sub!="name" and sub!="custom":
                    numOfProd += float(cookCart[key][sub])
                    order[key]["variations"][sub] = cookCart[key][sub]
        else:
            for variation in cookCart[key]["variations"]:
                customImages[variation] = 1
                order[key]["variations"][variation] = {
                    "numOfProd": 0,
                }
                for sub in cookCart[key]["variations"][variation]:
                    if sub!="src":
                        order[key]["variations"][variation]["numOfProd"] += float(cookCart[key]["variations"][variation][sub])
                        numOfProd += float(cookCart[key]["variations"][variation][sub])
                        order[key]["variations"][variation][sub] = cookCart[key]["variations"][variation][sub]


        


        order[key]["totalProd"] = numOfProd
        order[key]["totalPrice"] = numOfProd*float(prod.price)

        order["totalPrice"]+=order[key]["totalPrice"]

        

    client_secret = ""
    
    if not order["totalPrice"] == 0:
        intent = stripe.PaymentIntent.create(
            amount=int(order["totalPrice"]*100),
            currency='mxn',
            metadata={
                'integration_check': 'accept_a_payment',
                'myid': str(myUUID),
                'imagesUUIDS': json.dumps(customImages),
            },
        )
        client_secret = intent.client_secret
    else:
        cartHas = False
        

    
    
    if request.method == "POST":
        print("POST")
        try:
            objCheck = Order.objects.get(id=settings.ORDER_UUID)
            if objCheck != None:
                settings.ORDER_UUID = uuid.uuid4()
        except: 
            print("No obj found!")

        searchF = SearchForm(request.POST)
        form = CheckoutForm(request.POST)
        form1 = CheckoutForm1(request.POST)

        if searchF.is_valid():
            text1 = searchF.cleaned_data["text"]
            return redirect('/search/' + text1.lower())
        elif form1.is_valid() and form.is_valid():
            orderObj = Order(
                id=myUUID,
                total=float(intent.amount)/100,
                products=order
            )

            address = Address(
                order=orderObj,
                name=form.cleaned_data["name"],
                lastname=form.cleaned_data["lastname"],
                country=form.cleaned_data["country"],
                street=form.cleaned_data["street"],
                innerNum=form.cleaned_data["innerNum"],
                city=form.cleaned_data["city"],
                region=form.cleaned_data["region"],
                postalCode=form.cleaned_data["postalCode"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                shipping=False,
            )
            address1 = Address(
                order=orderObj,
                name=form1.cleaned_data["name"],
                lastname=form1.cleaned_data["lastname"],
                country=form1.cleaned_data["country"],
                street=form1.cleaned_data["street"],
                innerNum=form1.cleaned_data["innerNum"],
                city=form1.cleaned_data["city"],
                region=form1.cleaned_data["region"],
                postalCode=form1.cleaned_data["postalCode"],
                email=form1.cleaned_data["email"],
                phone=form1.cleaned_data["phone"],
                shipping=True,
            )

            orderObj.save()
            address.save()
            address1.save()

        elif form.is_valid():

            orderObj = Order(
                id=myUUID,
                total=float(intent.amount)/100,
                products=order
            )

            address = Address(
                order=orderObj,
                name=form.cleaned_data["name"],
                lastname=form.cleaned_data["lastname"],
                country=form.cleaned_data["country"],
                street=form.cleaned_data["street"],
                innerNum=form.cleaned_data["innerNum"],
                city=form.cleaned_data["city"],
                region=form.cleaned_data["region"],
                postalCode=form.cleaned_data["postalCode"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                shipping=True
            )

            orderObj.save()
            address.save()

    context={
        "form": SearchForm(),
        "client_secret": client_secret,
        "form1": CheckoutForm(),
        "form2": CheckoutForm1(),
        "cartHas": cartHas,
        "orderTotal": order["totalPrice"],
    }
    return render(request, 'checkout.html', context)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'payment_intent.succeeded':
        session = event['data']['object']
        orderID = session["metadata"]["myid"]
        order = Order.objects.get(id=uuid.UUID(orderID))
        order.status = "PN"
        order.save()
        receipt = StripeReceipt(
            order=order,
            receipt=json.loads(str(session))
        )
        receipt.save()
        
        for imgid in json.loads(session["metadata"]["imagesUUIDS"]):
            print(imgid)
            customimg = CustomImage.objects.get(uuid=uuid.UUID(imgid))
            customimg.status = "PN"
            customimg.save()

        address = Address.objects.filter(order=order).filter(shipping=True)


        context = {
            "name": address[0].name,
            "order": order,
        }

        subject, from_email, to = 'Pedido recibido. ID: '+ str(orderID), settings.EMAIL_HOST_USER, address[0].email
        html_content = render_to_string('orderEmail.html', context)
        text_content = strip_tags(html_content)
        msg = EmailMessage(subject, html_content, from_email, [to])
        msg.content_subtype = "html"  # Main content is now text/html

        with open(finders.find('images/white_logo-100x100.png'), 'rb') as f:
            logo_data = f.read()
        mime_image = MIMEImage(logo_data)
        mime_image.add_header('Content-ID', '<white_logo>')
        msg.attach(mime_image)
        msg.send()

    return HttpResponse(status=200)

def shipping(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())

    context = {
        "form": SearchForm(),
    }
    return render(request, "shippingPolicy.html", context)

def madeby(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text1 = form.cleaned_data["text"]
            return redirect('/search/' + text1.lower())

    context = {
        "form": SearchForm(),
    }

    return render(request, "madeby.html", context)