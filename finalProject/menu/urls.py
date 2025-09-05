from django.urls import path
from .views import *

urlpatterns = [
    path('', displayallitems, name="displayallitems"),
    path('Insert/', insertitem, name="insertitem"),
    path('Update/<int:id>', updateitem, name="updateitem"),
    path('Delete/<int:id>', deleteitem, name="deleteitem"),
    path('Search/', searchitem, name="searchitem")
]