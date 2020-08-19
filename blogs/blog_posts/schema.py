import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Post, Comment


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(ObjectType):
    post = graphene.Field(PostType, id=graphene.Int())
    posts = graphene.List(PostType)

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Post.objects.get(pk=id)
        return None

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()


class CommentInput(graphene.InputObjectType):
    id = graphene.ID()
    author = graphene.String()
    text = graphene.String()
    post = graphene.ID()


class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    publish_date = graphene.String()
    author = graphene.String()

    def resolve_publish_date(self, info):
        return str(self.publish_date)


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        post_instance = Post(title=input.title, description=input.description, publish_date=input.publish_date,
                             author=input.author)
        post_instance.save()
        return CreatePost(ok=ok, post=post_instance)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        post_instance = Post.objects.get(pk=id)
        if post_instance:
            ok = True
            if input.title:
                post_instance.title = input.title
            if input.description:
                post_instance.description = input.description
            if input.publish_date:
                post_instance.publish_date = input.publish_date
            if input.author:
                post_instance.author = input.author
            post_instance.save()
            return UpdatePost(ok=ok, post=post_instance)
        return UpdatePost(ok=ok, post=None)


class CreateComment(graphene.Mutation):
    class Arguments:
        input = CommentInput(required=True)

    ok = graphene.Boolean()
    comment = graphene.Field(CommentType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        comment_instance = Comment(
            author=input.author,
            text=input.text
        )
        comment_instance.post = Post.objects.get(id=input.post)
        comment_instance.save()
        return CreateComment(ok=ok, comment=comment_instance)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        try:
            comment_instance = Comment.objects.get(pk=id)
        except:
            comment_instance = None
        if comment_instance:
            ok = True
            comment_instance.delete()
        return DeleteComment(ok=ok)


class Mutation(graphene.ObjectType):
    createPost = CreatePost.Field()
    updatePost = UpdatePost.Field()
    createComment = CreateComment.Field()
    deleteComment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
