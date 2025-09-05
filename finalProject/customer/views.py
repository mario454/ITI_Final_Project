from django.shortcuts import render, redirect
from .models import Customer
from order.models import OrderItem, Order
from django.db import IntegrityError

# Create your views here.


def allcustomers(request):
    """
    View to list all customers with their number of orders.
    """
    context = {}
    customers = Customer.getallcustomers().order_by('id')
    numberoforders = [Order.objects.filter(customer=c).count() for c in customers]
    context['customers'] = zip(customers, numberoforders)

    return render(request, 'customer/list.html', context)

def viewcustorders(request, id):
        """
        View to display all orders and items for a given customer.
        Includes order details, items, total prices, and status choices to update it.
        """
        context = {}

        customer = Customer.getcustomerbyid(id)
        context['customer'] = customer
        context['orders'] = Order.getallordersbycustomer(customer=customer).order_by('order')
        context['ordersnitems'] = {order.order: OrderItem.getorderitemswithprice(orderid=order.order) for order in context['orders']}
        context['ordertotalprice'] = {order.order: OrderItem.calctotal(orderid=order.order)['total_price_order'] for order in context['orders']}
        context['STATUS_CHOICES'] = Order.STATUS_CHOICES  
        return render(request, 'customer/view.html', context)

def insertcust(request):
    """
    Handle customer creation form.

    - GET: Renders the customer insert form.
    - POST: Validates and creates a new customer if not already existing.
            If the customer exists, returns the form with an error message.

    Returns:
        Renders template or redirect to customer list.
    """
    if request.method == 'POST':
        name = request.POST['custname'].strip()
        phone = request.POST['custphone'].strip()
        if phone.startswith('+2'):
            phone = phone[2:]
        else:
            phone = phone
        email = request.POST['custemail'].strip()

        try:
            Customer.check_customer(name, phone)
            Customer.objects.create(
                name=name,
                phone=phone,
                email=email
            )
            return redirect('allcustomers') # POST and customer created successfully

        except ValueError:
            context={}
            context['error'] = "This customer exists before!"
            return render(request, 'customer/insert.html', context) # POST and customer exists before
        
    return render(request, 'customer/insert.html') # GET (FORM)
        

def updatecust(request, id):
    """
    Update customer details 
    - GET shows form
    - POST saves changes.
    """
    cust = Customer.getcustomerbyid(id)
    context = {'customer':cust}

    if request.method == 'POST':
        cust.name = request.POST['custname']
        cust.phone = request.POST['custphone']
        if cust.phone.startswith('+2'):
            cust.phone = cust.phone[2:]
        else:
            cust.phone = cust.phone
        cust.email = request.POST['custemail']
        cust.status = request.POST['custstatus'] == "Available"
        try:
            cust.save()
        except IntegrityError:
            context["error"] = "Phone Invalid"
            return render(request, 'customer/update.html', context)

        return redirect('allcustomers')
    
    return render(request, 'customer/update.html', context)

def deletecust(requset, id):
    """Soft delete customer by setting status to False."""

    Customer.objects.filter(id=id).update(status=False)
    return redirect('allcustomers')

    
def updateorder_st(request):
    """Update order status and redirect to customer orders view."""
    if request.method == "POST":
        order = Order.getorderbyid(request.POST['orderid_st'])
        order.status = request.POST['orstatus']
        order.save()
        return redirect('viewcustorders', id=request.POST['customerid_st'])