import graphene


#Specifying input = BookInput in the mutation of arguments
class BookInput(graphene.InputObjectType):
    title = graphene.String()
    author = graphene.String()
    year_published = graphene.String()
    review = graphene.String()

class CategoryInput(graphene.InputObjectType):
    name = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String()
    category = graphene.String()
    description = graphene.String()
    price = graphene.String()