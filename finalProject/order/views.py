from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Order, OrderItem
from customer.models import Customer
from menu.models import Item
# Create your views here.


def displayorder(request):
    """Display an order with its items, total price, and status choices."""
    orderid = request.session['context']['orderid']
    if orderid:
        print(orderid)
        context = {}
        context['order'] = Order.getorderbyid(orderid)
        context['orderitems'] = OrderItem.getorderitemswithprice(orderid)
        print(context['orderitems'])
        context['totalprice'] = OrderItem.calctotal(orderid= orderid)['total_price_order']
        context['STATUS_CHOICES'] = Order.STATUS_CHOICES

        return render(request, 'order/list.html', context)
    
    return render(request, 'order/list.html')


def createorder(request):
    """
    Handles order creation workflow based on the step provided.

    step (str): take customer value or order value
        - 'customer': 
            * Shows a pop-up in create.html to enter customer name and phone.
            * Calls createorder_customer() to create the customer if not existing
              and create a new order linked to them.
            * After creating, the view renders create.html in 'order' mode to allow
              adding items.

        - order:
            * Hides the customer pop-up.
            * Uses additemstoorder() to add items to the current order.

    Returns:
        Rendered 'order/create.html' with context:
            - If step='customer': customer pop up.
            - If step='order': order page with updated items.
    """
    context = {}
    if not request.session.get('context'):
        step = request.POST.get('step', '1')
        order = None
    else:
        step = request.session['context']['step']
        order = Order.getorderbyid(request.session['context']['orderid'])

    context['step'] = step
    context["error"] = None
    item = None
    if request.method == "POST":
        # If customer doesn't enter his data
        
        if step == '2':
            try:
                order = createorder_customer(request)
            except IntegrityError:
                context['error'] = "Customer with this phone number already exists."
                context['step'] = '1'
                context['name_error'] = request.POST['orcustname']
                context['phone_error'] = request.POST['orcustphone']

        # If customer enter data ->  enter items that added to items
        elif step == '3':
            item = additemstoorder(request, order)

    if order:      # Order Created
        context['order'] = order
        step = '3'
        context['step'] = '3'
        request.session['context'] = {
        'orderid': order.order,
        'step': '3',
        }
        if item:   # Items Added
            context['item'] = item

        return render(request, 'order/create.html', context)
    
    elif order == None and step == "2":
        print("here           2")
        context["step"] == "1"
        context["error"] = "Name or Phone is wrong!"
    
    return render(request, 'order/create.html', context)
    
    
    

def createorder_customer(request):
    """
    Creating order and creating customer if doesn't exist

    Returns: order linked to customer data
    """
    # Create customer if not exist
    custname = request.POST['orcustname'].strip().title()
    phone = request.POST['orcustphone'].strip()
    if phone.startswith('+2'):
        phone = phone[2:]
    else:
        phone = phone
    try:
        Customer.check_customer(custname,phone)
        Customer.objects.create(
            name = custname,
            phone = phone
        )
    except ValueError:
        pass
    except IntegrityError:
        raise IntegrityError
    
    custom = Customer.getcustomerbyphone_name(custname, phone)
    if not custom.status:
        custom.status = True
        custom.save()

    # Create Order for customer
    return Order.objects.create(
        customer = Customer.getcustomerbyphone_name(custname, phone)
    )

def additemstoorder(request, order):
    """
    Adding items to order which just created
    """
    try:
        order = Order.getorderbyid(order.order)
        item = Item.getitembyid(request.POST['oritemid'])
        quantity = int(request.POST['orquantity'])
        return OrderItem.objects.create(
            order = order,
            item = item,
            quantity = quantity
        )
    except IntegrityError:
        orderitem = OrderItem.getspecificitem(order=order, item=item)
        orderitem.quantity += quantity
        orderitem.save()
        return orderitem

def searchitemtoadd(request):
    """
    Handle search for menu items to add into an order.

    - If POST: filter items by name (case-insensitive, only active items).
    - If GET: return all items ordered by name.
    - Uses session to get current order and step information.
    - Renders the 'order/create.html' template with results.
    """
    context = {}
    name = ''
    if request.method == "POST":
        name = request.POST['search_item'].strip()
        context['items'] = Item.objects.filter(name__icontains=name, status=True).order_by('item')
    else:
        context['items'] = Item.objects.all().order_by('item')

    context['name'] = name

    addedcontext = request.session.get('context')
    context['order'] = Order.getorderbyid(addedcontext['orderid'])
    context['step'] = addedcontext['step']

    return render(request, f'order/create.html', context)


def updateorder(request):
    """
    Update the quantity of a specific item in an order.

    - POST only:
        * Get the order and item by their IDs.
        * Retrieve the corresponding OrderItem record.
        * Update its quantity and save.
    - Refreshes context with updated order details, order items (with prices), total order price, and status choices.
    - Renders the 'order/list.html' template.
    """
    # Check updates
    if request.method == 'POST':
        item = Item.getitembyid(request.POST['oritemid'])
        order = Order.getorderbyid(request.POST['orderid'])
        orderitem = OrderItem.getspecificitem(order=order, item=item)

        orderitem.quantity = request.POST['orquantity']
        orderitem.save()

        context = {}
        context['order'] = order
        context['orderitems'] = OrderItem.getorderitemswithprice(order.order)
        context['totalprice'] = OrderItem.calctotal(order.order)['total_price_order']
        context['STATUS_CHOICES'] = Order.STATUS_CHOICES

    return render(request, 'order/list.html', context)

def updateorder_finish(request):
    """
    Update order status on finish and clear session.

    - POST only:
        * Retrieve the order by ID.
        * Update its status.
        * Clear session context.
    Redirects to home page after saving.
    """
    # Check updates
    if request.method == 'POST':
        order = Order.getorderbyid(request.POST['orderid_finish'])
        order.status =  request.POST['orstatus']
        order.save()
        request.session.pop('context', None)

        return redirect('home')



def deleteitemorder(request, itemid):
    """
    Hard delete an item from the current order by its ID 
    and redirect back to the order display page.
    """

    OrderItem.objects.filter(item=itemid).delete()
    return redirect('displayorder')

def mostordered(request):
    """
    Return context containing the top 5 most ordered items.
    Used in homw page slider
    """
    context = {'MostOrdered': OrderItem.getmore_ordered_items()}
    return context