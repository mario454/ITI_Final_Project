from django.db import models
import re
# Create your models here.

class Customer(models.Model):
    """
    Model representing a customer in the restaurant management system.

    Fields:
        name (str): Full name of the customer. Maximum length 100 characters. Required.
        phone (str, uniqueness): Customer's phone number. Maximum length 11 characters. Required.
        email (str, optional): Customer's email address. Maximum length 50 characters. Optional.
    
    Constraints:
        - Composite unique key on (name, phone) to ensure each phone appears only once per name.

    Relationships:
        - One-to-Many: Customer -> Orders
    
    Class Methods:
        getallcustomers(): Returns all Customer objects in the database.
        getcustomerbyphone(phone): Returns the Customer object with the specified phone number.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=13, null=False, unique=True)
    email = models.EmailField(max_length=50, null=True)
    status = models.BooleanField(default=True)

    # Make Composite Key of name & phone
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'phone'], name='unique_customer')
    ]
    
    @classmethod
    def getallcustomers(cls):
        """
        return: QuerySet containing all Customer Objects from the database.
        """
        return cls.objects.all()
    
    @classmethod
    def getcustomerbyid(cls, id):
        """
        return: Customer object with given id
        """
        return cls.objects.get(id=id)
    
    @classmethod
    def check_customer(cls, name, phone):
        """
        Check if a customer with the given name and phone number already exists.

        Args:
            name (str): The name of the customer.
            phone (str): The phone number of the customer.

        Raises:
            ValueError: If a customer with the same name and phone already exists.

        Returns:
            bool: True if no such customer exists (safe to create).
        """
        if Customer.objects.filter(name=name, phone=phone).exists():
            raise ValueError
    

    
    @classmethod
    def getcustomerbyphone_name(cls, name, phone):
        """
        Retrieve a customer by matching both name and phone number.

        Args:
            name (str): The name of the customer.
            phone (str): The phone number of the customer.

        Raises:
            ValueError: If no customer exists with the given name and phone.

        Returns:
            Customer: The customer object matching the given name and phone.
        """
        if not Customer.objects.filter(name=name, phone=phone).exists():
            raise ValueError
        
        return cls.objects.get(name=name, phone=phone)
        