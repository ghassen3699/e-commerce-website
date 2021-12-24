import json
from django.shortcuts import render
from .models import *
from django.http import JsonResponse


def store(request) :
    products = Product.objects.all()

    if request.user.is_authenticated:
        order,created = Order.objects.get_or_create(customer = request.user.costumer, complete=False)
    else :
        order = {'total_items':0,'shipping':False}
    return render(request,"store/store.html",{'products':products,'order':order})



def cart(request) :
    if request.user.is_authenticated:
        costumer = request.user.costumer
        order,created = Order.objects.get_or_create(customer = costumer, complete=False)
        items = order.orderitem_set.all()
    else :
        items = []
        order = {'total_cart':0,'total_items':0,'shipping':False}
    return render(request,'store/cart.html',{'items':items,'order':order})



def checkout(request) :
    if request.user.is_authenticated:
        costumer = request.user.costumer
        order,created = Order.objects.get_or_create(customer = costumer, complete=False)
        items = order.orderitem_set.all()
    else :
        items = []
        order = {'total_cart':0,'total_items':0,'shipping':False}

    return render(request,'store/chekout.html',{'items':items,'order':order})



def updateItem(request) :
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']


    customer = request.user.costumer 
    product = Product.objects.get(id = productId)
    order,created = Order.objects.get_or_create(customer = request.user.costumer, complete=False)
    orderItem , created = OrderItem.objects.get_or_create(order = order, product=product)

    if action == "add" :
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove" :
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0 :
        orderItem.delete()
        
    return JsonResponse('Item was added',safe=False)