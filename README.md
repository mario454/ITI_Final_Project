# Title: Django Restaurant Management System
## Name: Everest Cuisine
## Video Demo:  [[youtube video](https://youtu.be/NY7KezwHg6w?si=U563QnuecfbeZ9Vq](https://youtu.be/76OQgVX9qqw?si=KqGyDLAI95GqhdGH))

### Description
- Full-stack Python project using **Django** as the framework and **PostgreSQL** as the DBMS.  
- Helps manage restaurant operations such as **creating orders**, **displaying the menu**, **updating order quantities**, and more, organized through `three` apps: **Menu**, **Customer**, and **Order**.


### Libraries
#### 1- Python Libraries 
>All needed libraries in requirements.txt can install it by

```bash
pip install -r requirements.txt
```
#### 2- Front-end Libraries
- ***AOS Library*** used in `fade out` affect - can show it in **base.html** and **templates/menu/list.html**
```html
<link href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet">  

<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
```

- ***Bootstrap Library*** used in Most ordered items carousel slider in **base.html**
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"> 
-> above link not used fully to avoid affecting other styles; only extract carousel slider CSS
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

### Apps

#### Menu App:
The **Menu App** allows you to:  
- Display existing items with their details.  
- Insert new items into the menu.  
- Update or delete existing items.  


##### Display Existing Items (`displayallitems` function) through *menu/list.html*
Displays all menu items with the following details:  
- Item number  
- Item name  
- Price  
- Description  
- Image  
- Status (Available / Not Available).

##### Insert New Items (`insertitem` function)
- Insert new menu items through `menu/insert.html`.

##### Update Existing Items (`updateitem` function)
- Update existing menu items through `menu/update.html`.

##### Soft Delete for Existing Items (`deleteitem` function)
- Perform a soft delete by changing the availability status of items through `menu/list.html`.


#### models.py
Contains the `Item` class, which translates to a table in the database.

##### Item Class Fields:
- `item` (Primary Key)  
- `name`  
- `price`  
- `description` (Optional)  
- `image` (Optional)  
- `status` (Default = `True` → Available)

##### Item Class Classmethods
- `getallitems` – Retrieves all records from the `Item` table in the database.  
- `getitembyid` – Retrieves a specific record from the `Item` table by its ID.


#### urls.py
Contains all URL patterns used for routing paths in the project for the **Menu App**.

#### Templates
##### Insert Template
- **Nav bar** – Facilitates navigation between the list of items and the insert form.  
- **Insert Form** – Used to add new items to the menu.

##### Update Template
- **Update Form** – Used to update a specific item from the list of items.

##### List Template
- **Nav bar** – Facilitates navigation between the list of items and the insert form.  
- **Search Form** – Used to search for items containing a substring (case-insensitive).  
- **List as Table** – Displays item details and allows control via **Delete** and **Update** buttons.

---

#### Customer App:
The **Customer App** allows you to:  
- Display existing customers with their details.  
- Insert new customers.  
- Update or delete existing customers.


##### Display Existing Customers (`allcustomers` function) through *customer/list.html*
Displays all menu items with the following details:  
- Name
- Phone
- Email
- Orders Count
- Status (Active / Inactive)

#### View Customer Orders (`viewcustorders` function)
- View all orders of a customer through `customer/view.html`.  
- Displays order details including:
  - Order details
  - *All items* with their quantity in the order
  - Total price  
  - Status (`pending`, `confirmed`, `cancelled`)  

##### Insert New customers (`insertcust` function)
- Insert new customers through `customer/insert.html`.

##### Update Existing Customers (`updateitem` function)
- Update existing customers through `menu/update.html`.

##### Soft Delete for Existing Items (`deleteitem` function)
- Perform a soft delete by changing the availability status of items through `menu/list.html`.


#### Update Order Status (`updateorder_st` function)
- Changes the status of an order and saves it to the database.

#### models.py
Contains the `Customer` class, which translates to a table in the database.

#### Fields
- `id` (Primary Key)  
- `name`  
- `phone` (unique)
- `email` (Optional)  
- `status` (Default = `True` → Active)  
- Composite unique key on `(name, phone)` to ensure that each combination of name and phone is unique per customer.


##### Customer Class Classmethods
- `getallcustomers` – Retrieves all records from the `Customer` table in the database.  
- `getcustomerbyid` – Retrieves a specific record from the `Customer` table by its ID.  
- `getcustomerbyphone_name` – Retrieves a specific record from the `Customer` table by its **name** and **phone**.  
- `check_customer` – Checks if a customer already exists and raises a `ValueError` if found, to be handled in `views.py` functions.


#### urls.py
Contains all URL patterns used for routing paths in the project for the **Customer App**.

#### Templates

##### Insert Template
- **Nav bar** – Facilitates navigation between the list of customers and the insert form.  
- **Insert Form** – Used to add new customers.


##### Update Template
- **Update Form** – Used to update a specific customer from the list of customers.

##### List Template
- **Nav bar** – Facilitates navigation between the list of items and the insert form.  
- **Search Form** – Used to search for items containing a substring (case-insensitive).  
- **Table**
    - Displays item details
    - Allows control via **Delete** and **Update** buttons.  
    - **view** button link this page with `view.html` to display the orders with detaisl for a specific customer.

#### View Template
- View all orders with details of a customer.  
- Displays order details including:
  - Order number  
  - Total price of the order  
  - Status (`pending`, `confirmed`, `cancelled`) of each order with the ability to change it  
  - *All items* with their quantity in the order displayed in a table

#### Template Tag folder
Used to create a custom access method in Django templates to access dictionary values by key.  

```django
{% for orderitem in ordersnitems|keyvalue:order.order %}
```

---

### Order App
The **Order App** allows you to:  
- Create a new order.  
- Add items to an order.  
- Display existing items in an order.  
- Update or delete the order status or its items.


##### Create Order (`createorder` function) through *order/create.html*
- `createorder_customer` function – Creates a new order without items. Connects the order with a specific customer if they exist; otherwise, creates a new customer.  
- `additemstoorder` function – Adds items to an open order.

##### Search Items (`searchitemtoadd` function) through *order/create.html*
- Searches for items to add to an order, similar to the functionality in the **Menu App**.

##### Display Order (`displayorder` function) through *order/list.html*
- Displays order details including:
  - Total price  
  - Status  
  - Items in this order

#### Update Order Details (`updateorder` function) through *order/list.html*
- Updates order **status**.  
- Updates items in the order by deleting them or increasing/decreasing their quantity.

#### Delete Item from Order (`deleteitemorder` function) through *order/list.html*
- Performs a hard delete of an item from the order.


#### View Most Ordered Items (`mostordered` function) through *base.html*
- Displays the most ordered items and their details.


#### models.py
- Contains the `Order` class, which translates to a table in the database and is related to the **Customer** and **Item** classes.  
- Contains the `OrderItem` class, which translates to a table representing the many-to-many relationship between **Order** and **Item**.

#### `Order Class`
#### Order Fields
- `order` (Primary Key)
- `createdTime` – Timestamp of order creation  
- `status` – Order status with choices: `pending`, `confirmed`, `cancelled`  
- `customer` – ForeignKey to the **Customer** class (1-to-many relationship)  
- `items` – Many-to-many relationship with the **Item** class through the `OrderItem` table


##### Order Class Classmethods

- `getorderbyid` – Retrieves a specific record from the `Order` table by its ID. 

- `getorderbycustomer` – Retrieves all orders for a specific customer from the `Order` table.



#### `OrderItem Class`
Intermediate model representing the **many-to-many relationship** between **Order** and **Item**.

#### OrderItem Fields
- `order` – ForeignKey to the related **Order**. Deleting the Order will delete the OrderItem (CASCADE).  
- `item` – ForeignKey to the related **Item**. If the Item is deleted, set to NULL.  
- `quantity` – Number of this item in the order. Default is 1.  

- Composite unique key on `(order, item)` to ensure each item appears only once per order.

#### Class Methods
- `getspecificitem(order, item)` – Returns a specific item in a specific order.  

- `getorderitemswithprice(orderid)` – Returns all items in the specified order with `total_price_item = quantity * item.price`. 

- `calctotal(orderid)` – Calculates the total price of the order by summing `quantity * item.price`. 

- `getmore_ordered_items()` – Retrieves the **top 3 most ordered items** based on confirmed orders, including:
  - `item__name`  
  - `item__image`  
  - `item__price`  
  - `total_ordered` (sum of quantities)  
  Only considers items with `status=True` and `image` not null, sorted in *descending* order of `total_ordered`.

#### urls.py
Contains all URL patterns used for routing paths in the project for the **Order App**.

#### Templates

##### Create Template
- **Insert Form** – Links order creation with a customer.  
- **Search Bar** – Used to search for items to add to the order.  
- **List as Table** – Displays *available* items with controls to adjust the quantity of each item and can add this item with quantity using the **Add** button.

- **View Order Button** – Navigates to `list.html` to display the order information.

##### List Template
- **Customer Information Fieldset** – Displays customer information for this order.  
- **Order Information** – Shows total price and allows changing the status of the order.  
- **Table**
  - Displays item details.  
  - Allows control via **Delete** and **Update** buttons.  
  - **Update** button confirms changes in the quantity of a specific item.  

- **Done Button** – Completes the order.

---

### base.html
The main layout template for the project.

```python
def homepage(request):
    context = mostordered(request)
    print(context)
    return render(request, 'base.html', context)
```

- **Header** – Contains the logo, restaurant name, and a navigation bar for all project pages.  

- **Main** – Dynamic content area that changes per page:
  - Slider using **Bootstrap** to display the top three most ordered items.  
  - Paragraphs describing the restaurant.  

- **Footer**:
  - **Contact Table** – Includes address link, phone number, and opening hours.  
  - **Quick Links** – Navigation bar for all project pages.  
  - **Social Media** – Links to all social media platforms.


---

### Admin Dashboard:
#### manager:
- Username: manager
- email: manager@gmail.com
- password: manager

#### Edit Menu:
- Username: editMenu
- email: menu@gmail.com
- password: _LB.Jh9S.zb6Ju7

#### Edit Customers:
- Username: editCustomers
- email: customers@gmail.com
- password: d7CHY6RZwhjV2w.

#### Edit Orders:
- Username: editOrders
- email: orders@gmail.com
- password: z59NpDFL.dq86ef


