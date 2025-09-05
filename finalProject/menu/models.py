from django.db import models

# Create your models here.

class Item(models.Model):
    """
    Model representing an item on the menu in the restaurant management system.

    Fields:
        item (int): Primary key of the item (AutoField).
        name (str): item's. Maximum length 100 characters. Required.
        price (float): item's price. Required.
        description (str, optional): item's description. Maximum length 200 characters. Optional.

    Relationships:
        - Many-to-Many: Item -> Order (through OrderItem)
    """
    item = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    price = models.FloatField(null=False)
    description = models.TextField(max_length=200, null=True)
    image = models.ImageField(upload_to='menu_images/', default=None)
    status = models.BooleanField(default=True)

    @classmethod
    def getallitems(cls):
        """
        return: QuerySet containing all item objects saved in the database.
        """
        return cls.objects.all()
    
    @classmethod
    def getitembyid(cls, id):
        """
        id: int
        return: Item object with the given primary key (id)
        """
        return cls.objects.get(item=id)