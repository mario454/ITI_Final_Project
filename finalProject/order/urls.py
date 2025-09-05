from django.urls import path
from .views import *

urlpatterns = [
    path('', createorder, name="createorder"),
    path('Search-Add/', searchitemtoadd, name="searchitemtoadd"),
    path('Display/', displayorder, name="displayorder"),
    path('Update/', updateorder, name="updateorder"),
    path('Delete/<int:itemid>', deleteitemorder, name="deleteitemorder"),
    path('Base/', updateorder_finish, name="updateorder_finish")
]