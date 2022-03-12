from unicodedata import category
import graphene

from graphene_django import DjangoObjectType, DjangoListField 
from .modeltype import *
from .modelinput import *


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        year_published = graphene.String(required=True)
        review = graphene.String(required=True)

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls,root,info,**kwargs):
        book = Book.objects.create(
            title=kwargs.get('title'),
            author=kwargs.get('author'),
            year_published=kwargs.get('year_published'),
            review=kwargs.get('review')
        )

        return CreateBook(book=book)

class UpdateBooks(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID()

    books = graphene.Field(BookType)


    @classmethod
    def mutate(cls,root,info,title,id):
        book = Book.objects.get(id=id)
        book.title = title
        book.save()

        return UpdateBooks(books=book)

class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CategoryInput(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,input):
        category = Category.objects.create(
            name=input.name
        )
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    class Arguments:
        id= graphene.ID(required=True)
        name= graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,**kwargs):
        id = kwargs.get('id',None)
        name = kwargs.get('name',None)

        if id and name is None:
            return None

        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return UpdateCategory(category=category)

class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,id):
        category = Category.objects.get(id=id)
        category.delete()
        return DeleteCategory(category=category)


class Mutation(graphene.ObjectType):
    update_book = UpdateBooks.Field()
    create_book = CreateBook.Field()

    update_category = UpdateCategory.Field()
    create_category = CreateCategory.Field()
    delete_category = DeleteCategory.Field()

class Query(graphene.ObjectType):

    books = graphene.List(BookType)
    one_books = graphene.Field(BookType, id=graphene.String(required=True))

    category = graphene.List(CategoryType)
    one_category = graphene.Field(CategoryType, id=graphene.String(required=True))

    def resolve_books(root, info, **kwargs):
        return Book.objects.all()
    
    def resolve_one_books(root, info, **kwargs):
        id = kwargs.get("id")
        try:
            return Book.objects.filter(id=id).first()
        except:
            return None

    def resolve_category(root, info, **kwargs):
        return Category.objects.all()

    def resolve_one_category(root, info, **kwargs):
        id = kwargs.get("id")
        try:
            return Category.objects.filter(id=id).first()
        except:
            return None

schema = graphene.Schema(query=Query,mutation=Mutation)

