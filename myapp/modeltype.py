import graphene

from graphene_django import DjangoObjectType
from .models import *

class ProductsType(DjangoObjectType):
    class Meta:
        model = Products
        fields = '__all__'

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"