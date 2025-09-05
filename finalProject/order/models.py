from django.db import models
from menu.models import Item
from customer.models import Customer
from django.db.models import Sum, F, Q
# Create your models here.

class Order(models.Model):
    """
    Model representing a customer's order in the restaurant management system.

    Fields:
        order_id (int): Primary key for the order (AutoField).
        created_time (datetime): Timestamp when the order was created.
        status (boolean): False(default): If order is pending or not confirmed, True: If order confirmed

    Relationships:
        customer (ForeignKey): One-to-Many relationship with Customer.
            - Each order belongs to one customer.
            - Deleting the customer will delete all their orders (CASCADE).

        items (ManyToManyField): Many-to-Many relationship with Item (through OrderItem).
            - Each order can have multiple items.
            - Each item can belong to multiple orders.
            - The intermediate table (OrderItem) stores quantity information.

    Class Methods:
        getallorders(): Returns all Order objects in the database.
        getorderbyid(id): Returns the Order object with the specified primary key.
        getorderbytime(day): Returns all orders created on the given date.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    order = models.AutoField(primary_key=True) # Order id
    CreatedTime = models.DateTimeField(auto_now_add=True) # Get time of order creation
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) # Make 1-n relationship with customer
    items = models.ManyToManyField(Item, through='OrderItem') # Make n-n relationship with item, and (through = ) result table called  OrderItem
    
    @classmethod
    def getorderbyid(cls, id):
        """
        id: int
        return: Order object with the given primary key (id)
        """
        return cls.objects.get(order=id)
    
    @classmethod
    def getallordersbycustomer(cls, customer):
        """
        customer: customer id
        return: QuerySet of all orders for this customer
        """
        return cls.objects.filter(customer=customer)


# Class OrderItem result of many to many relationship between order and item 
class OrderItem(models.Model):
    """
    Intermediate model representing the relationship -Many to Many- between Order and Item.

    Fields:
        order (ForeignKey): Reference to the related Order. Deleting the Order will delete the OrderItem (CASCADE).
        item (ForeignKey, nullable): Reference to the related Item. If the Item is deleted, set to NULL.
        quantity (int): Number of this item in the order. Default is 1.

    Constraints:
        - Composite unique key on (order, item) to ensure each item appears only once per order.

    Class Methods:
        getorderitems(order): Returns a QuerySet of all items in the specified order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    # To make composite key for OrderItem to be unique per order and item
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'item'], name='unique_order_item')
        ]
    
    @classmethod
    def getspecificitem(cls, order, item):
        """
        order: order id
        return: Queryset of all items which in this order
        """
        return cls.objects.get(order=order, item=item)

    @classmethod
    def getorderitemswithprice(cls, orderid):
        """Return all items in the order annotated with total price per item."""
        return cls.objects.filter(order__order=orderid).annotate(
            total_price_item=F('quantity') * F('item__price')
        ).order_by('item')

    @classmethod
    def calctotal(cls, orderid):
        """Calculate and return the total price of the order."""
        return cls.objects.filter(order__order=orderid).aggregate(total_price_order=Sum(F('quantity') * F('item__price')))

    # Get more 5 items ordered in all orders 
    @classmethod
    def getmore_ordered_items(cls):
        """
        Retrieve the top 5 most ordered items based on confirmed orders.

        This method:
        - Make new field `total_ordered` that aggregates the total quantity ordered for each item.
        - Considers only orders where `order__status='confirmed'`.
        - Returns a queryset of dictionaries with keys:
                - 'item' (the item ID or field)
                - 'total_ordered' (the summed quantity)
        - Results are sorted in descending order by 'total_ordered'.
        - Limited to the top 5 items. `order_by('-total_ordered')[:5]`

        Returns:
            QuerySet[dict]: A queryset of dictionaries, each containing:
                {
                    'item': item id,
                    'total_ordered': sum of quantities
                }
        """
        return (
        cls.objects
        .filter(item__status=True, item__image__isnull = False)
        .values("item__name", "item__image", "item__price")
        .annotate(total_ordered=Sum("quantity"))
        .order_by("-total_ordered")[:3]
    )
    
    