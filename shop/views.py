from logging import exception
from shop.models import Product, Contact, Orders, OrderUpdate
from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
import json

from django.views.decorators.csrf import csrf_exempt

# MERCHANT_KEY = 'Your-Merchant-Key-Here'
MERCHANT_KEY = 'bKMfNxPPf_QdZppa'
# Create your views here.
def shop_home(request):
    # P = Product.objects.get(product_name = 'Mac Book Pro')
    # p_name = P.product_name
    # cat = P.category
    # s_cat = P.subcategory
    # price = P.price
    # dis = P.discription
    # P_date = P.publish_date
    # _img = P.image
    # d = {
    #         "Product_Name": p_name,
    #         "Category": cat,
    #         "S_Category": s_cat,
    #         "Price": price,
    #         "Discription": dis,
    #         "Publish_Date": P_date,
    #         "image": _img
    #     }

    # get all products
    products = Product.objects.all()
    print(products)
    # # nubmers of items in products
    # n = len(products)
    # print(n)
    # n_slides = n//4 + ceil((n//4) - (n//4))
    # print(n_slides)
    # l = [[products, range(1,n_slides), n_slides], [products, range(1,n_slides), n_slides]]
    # data = {
    #     'allProducts': l
    # }

    allproducts = []
    # get categories name
    cat_products = Product.objects.values('category', 'id')
    print(cat_products)
    # store values of categories in a  set to remove duplications
    cats = {item['category'] for item in cat_products}
    print(cats)
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        print(prod)
        n = len(prod)
        n_Slide = n // 4 + ceil ((n // 4) - (n // 4))
        allproducts.append([prod, range(1, n_Slide), n_Slide])
    
    data = {"allProducts" : allproducts}
    print(data )
    return render(request,'shop/home.html', data)

def shop_about(request):
    return render(request, 'shop/about.html')

def shop_contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})
    

def shop_tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id = orderId, email = email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id = orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                    return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html')


def productView(request, myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request, "shop/pView.html", {'product': product[0]})



def shop_checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id

        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')

def shop_login(request):
    return render(request, 'shop/login.html')

def shop_signup(request):
    return render(request, 'shop/signup.html')

def searchMatch(query, item):
    if query in  item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


