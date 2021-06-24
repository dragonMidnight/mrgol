from django.contrib.auth.models import Group
#from django.template.defaultfilters import slugify      this  slugify has not allow_unicode argument(from git)    
from django.utils.text import slugify


from rest_framework import serializers

from .models import Comment, Content, Post, Rating, Product, Image, Root, Filter_Attribute
from users.myserializers import UserNameSerializer
from users.myserializers import UserSerializer



class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
       
class CommentSerializer(serializers.ModelSerializer):
    author = UserNameSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'




class RootListSerializer(serializers.ModelSerializer):         #note RootListSerializer should be before PostListSerializer
    url = serializers.SerializerMethodField()
    strg = serializers.SerializerMethodField()
    
    class Meta:
        model = Root
        fields = '__all__'
    
    def get_url(self, obj):
        return '/{}/{}/'.format(obj.id, slugify(obj.name, allow_unicode=True))

    def get_strg(self, obj):
        return obj.__str__()




class Filter_AttributeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter_Attribute
        fields = '__all__'
    


    
class PostListSerializer(serializers.ModelSerializer):
    root = RootListSerializer()
    image_icon = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'root',  'brief_description', 'image_icon', 'url', 'published_date']

    def get_image_icon(self, obj):
        request = self.context.get('request', None)
        try:
            url = request.build_absolute_uri(obj.image_icon.url)             #request.build_absolute_uri()  is like "http://127.0.0.1:8000/product_list/"     and   request.build_absolute_uri(obj.image_icon.url) is like:  "http://192.168.114.6:8000/product_list/media/3.jpg" (request.build_absolute_uri() + obj.image_icon.url)   
        except:
            url = ''                                                         #if obj have not image(obj.image_icone was blank) this line will run.
        return url

    def get_url(self, obj):
        pk, slug = obj.id, obj.slug
        return f'{pk}/{slug}/'

    


class ProductListSerializer(serializers.ModelSerializer):
    root = RootListSerializer()
    image_icon = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    rating = RatingSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['title', 'root', 'image_icon', 'url', 'available', 'rating', 'price']

    def get_image_icon(self, obj):
        request = self.context.get('request', None)
        try:
            url = request.build_absolute_uri(obj.image_icon.url)
        except:
            url = ''
        return url

    def get_url(self, obj):
        pk, slug = obj.id, obj.slug
        return f'{pk}/{slug}/'




    
class PostDetailSerializer(serializers.ModelSerializer):
    author = UserNameSerializer()
    root = RootListSerializer()    
    contents = ContentSerializer(many=True)
    comment_set = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = '__all__'


  

class ProductDetailSerializer(serializers.ModelSerializer):
    root = RootListSerializer()    
    rating = RatingSerializer(read_only=True)
    comment_set = CommentSerializer(read_only=True, many=True)
    image_set = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'




     
        
