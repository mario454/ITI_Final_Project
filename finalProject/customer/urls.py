from django.urls import path
from .views import *

urlpatterns = [
    path('', allcustomers, name="allcustomers"),
    path('View/<int:id>', viewcustorders, name="viewcustorders"),
    path('Insert/', insertcust, name="insertcust"),
    path('Update/<int:id>', updatecust, name="updatecust"),
    path('Delete/<int:id>', deletecust, name="deletecust"),
    path('stupdate/', updateorder_st, name="updateorder_st")
]