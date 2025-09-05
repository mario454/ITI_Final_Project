from django.shortcuts import render, redirect
from .models import Item

# Create your views here.

def displayallitems(request):
    """Render a list of all menu items, ordered by the 'item' field."""
    context = {}
    context['items'] = Item.getallitems().order_by('item')
    return render(request, 'menu/list.html', context)


def insertitem(request):
    """Handle insertion of a new menu item and render the insert page."""
    context = {}
    if request.FILES.get('itimage'):
        context['imagename'] = request.FILES.get('itimage').name

    if request.method == "POST":
        Item.objects.create(
            name = request.POST['itname'],
            price = request.POST['itprice'],
            description = request.POST['itdescription'],
            image = request.FILES.get('itimage')
        )
        return redirect('displayallitems')
    
    return render(request, 'menu/insert.html', context)


def updateitem(request, id):
    """
    Update an existing item's details and render the update form.

    Handles POST requests to update the item's name, price, description, 
    status, and optional image. On GET requests, displays the current 
    item data in the update form.
    """
    item = Item.getitembyid(id)
    context = {'item': item}
    if request.method == "POST":
        item.name = request.POST['itname']
        item.price = request.POST['itprice']
        item.description = request.POST['itdescription']
        item.status = request.POST['itstatus'] == "Available"
        if request.FILES.get('itimage'):
            item.image = request.FILES['itimage']
        item.save()

        return redirect('displayallitems')
    
    return render(request, 'menu/update.html', context)


def deleteitem(request, id):
    """Soft-delete an item by setting its status to False and redirect to the item list."""
    Item.objects.filter(item=id).update(status=False)
    return redirect('displayallitems')



# Search about items
def searchitem(request):
    """
    Search for items by name and render the list page.

    Handles POST requests to filter items whose names contain the 
    search term (case-insensitive). On GET requests, displays all items.
    """
    context = {}
    name = ''
    if request.method == "POST":
        name = request.POST['search_item']
        context['items'] = Item.objects.filter(name__icontains=name).order_by('item')
    else:
        context['items'] = Item.objects.all().order_by('item')
    context['name'] = name

        
    return render(request, f'menu/list.html', context)


# # API using Django: Search about items
# def searchitem_api(request, name):
#     name = name.strip()
#     if name:
#         items = Item.objects.filter(name__icontains=name)
#     else:
#         items = Item.objects.all()
#     results = [{'id': item.id, 'name': item.name, 'price': item.price} for item in items]
#     return JsonResponse({'items': results})


