import graphene
from graphene_django import DjangoObjectType

from api.models import Post, Comment

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "body", "owner")

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "body", "owner", "post")

# Query

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.ID())
    all_comments = graphene.List(CommentType)
    comment = graphene.Field(CommentType, id=graphene.ID())

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_post(root, info, id):
        return Post.objects.get(pk=id)

    def resolve_all_comments(root, info):
        return Comment.objects.all()

    def resolve_comment(root, info, id):
        return Comment.objects.get(pk=id)


# Mutation

class CreatePost(graphene.Mutation):
    class Arguments:
        created = graphene.types.datetime.DateTime()
        title = graphene.String()
        body = graphene.String()
        
    
    post = graphene.Field(PostType)

    def mutate(self, info, created=None, title=None, body=None):
        

        post = Post.objects.create(
            created = created,
            title = title,
            body = body,
            owner = info.context.user
        )

        post.save()
        return CreatePost(post = post)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        created = graphene.types.datetime.DateTime()
        title = graphene.String()
        body = graphene.String()
        owner = graphene.List(graphene.ID)

    post = graphene.Field(PostType)

    def mutate(self, info, id, created=None, title=None, body=None, owner = None):
        post = Post.objects.get(pk=id)
        post.created = created if created is not None else post.created
        post.title = title if title is not None else post.title
        post.body = body if body is not None else post.body
        post.owner = owner if owner is not None else info.context.user

        if owner is not None:
            owner_set = []
            for id in owner:
                owner_object = Post.objects.get(pk=id)
                owner_set.append(owner_object)
            post.owner.set(owner_set)

        post.save()
        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    post = graphene.Field(PostType)
    
    def mutate(self, info, id):
        post = Post.objects.get(pk=id)
        if post is not None:
            post.delete()
        return DeletePost(post = post)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)