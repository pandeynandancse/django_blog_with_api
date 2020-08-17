from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )


from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentSerializer
from comments.models import Comment

from posts.models import Post


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            #'id',
            'title',
            #'slug',
            'content',
            'publish'
        ]


post_detail_url = HyperlinkedIdentityField(
        view_name='posts-api:detail', #posts-api has been taken from urls.py defined inside bolg/ i.e. project name  as a namespace ==>> 'detail'  has been taken from urls.py defined inside urls.py in posts/api as a name 
        lookup_field='slug'  #by defualt is primary key but we customized it to slug field
        )


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    # user = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Post


        #anything we defined above such that url , user ,image,html , comments must be defined inside fields list to show it.
        fields = [
            'url',
            'id',
            'user',
            'title',
            'slug',
            'content',
            'html',
            'publish',
            'image',
            'comments',
        ]


    # below defined all functions are overrided
    def get_html(self, obj):  #to show html 
        return obj.get_markdown()

    def get_image(self, obj):  #to show image url
        try:
            image = obj.image.url
        except:
            image = None
        return image


    #remove this function if using user = UserDetailSerializer(read_only=True)
    # def get_user(self,obj):  #to show user
    #     return str(obj.user.username)

    def get_comments(self, obj):  #to show comment
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments



class PostListSerializer(ModelSerializer):
    url = post_detail_url
    delete_url = HyperlinkedIdentityField(
            view_name = 'posts-api:delete',
            lookup_field= 'slug'
        )
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'content',
            'publish',
            'delete_url'
        ]




""""

from posts.models import Post
from posts.api.serializers import PostDetailSerializer


data = {
    "title": "Yeahh buddy",
    "content": "New content",
    "publish": "2016-2-12",
    "slug": "yeah-buddy",
    
}

obj = Post.objects.get(id=2)
new_item = PostDetailSerializer(obj, data=data)
if new_item.is_valid():
    new_item.save()
else:
    print(new_item.errors)


"""