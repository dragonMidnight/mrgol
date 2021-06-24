from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models

from datetime import datetime

from users.models import User
#note: changing classes places may raise error when creating tables(makemigrations), for example changing Content with Post will raise error(Content use Post in its field and shuld be definded after Post)


class Root(models.Model):                                  #note: supose roor2 object,  root2.father_root determine father of root2 and root2.root_set is list of root2's childer,  root with level=1 can has eny father!
    name = models.CharField(unique=True, max_length=25, verbose_name='نام' if settings.ERROR_LANGUAGE=='pr' else 'name')
    slug = models.SlugField(allow_unicode=True, db_index=False, verbose_name='آدرس وب' if settings.ERROR_LANGUAGE=='pr' else 'slug')
    level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], verbose_name='سطح' if settings.ERROR_LANGUAGE=='pr' else 'slug')        #important: PositiveSmallIntegerField only should be in root.level why? because we used PositiveSmallIntegerField as edentifier of root.level in admin.py/def change_view
    father_root = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='ريشه پدر' if settings.ERROR_LANGUAGE=='pr' else 'father root')        #if root.level>1 will force to filling this field.
    post_product = models.CharField(max_length=10, default='product', verbose_name='کالا يا پست' if settings.ERROR_LANGUAGE=='pr' else 'post or product')      #this should be radio button in admin panel.
    #root_set
    
    class Meta:
        ordering = ('level', '-father_root_id')                    #-father_root_id  will make childs with same father be in together. and '-' will make decending order like ordering django admin for 'order by ids' means lower ids will go to down.(tested)
        verbose_name = 'ريشه' if settings.ERROR_LANGUAGE=='pr' else 'root'
        verbose_name_plural = 'ريشه ها' if settings.ERROR_LANGUAGE=='pr' else 'roots'
        
    def __str__(self):
        return str(str(self.level) + ' - ' + self.name)
    
    def clean_fields(self, exclude=None):
        if self.level > 1 and not self.father_root:
            raise ValidationError({'father_root': [_('برای سطح بالاتر از 1 اين قسمت ضروري است.') if settings.ERROR_LANGUAGE=='pr' else _('This field is required for level more than 1.')]})
        super().clean_fields(exclude=None)
    '''
    def save(self, *args, **kwargs):
        create_Rating = False
        if self.level > 1:
            raise ValidationError({'father_root': ['برای سطح بالاتر از 1 اين قسمت ضروري است.' if settings.ERROR_LANGUAGE=='pr' else 'This field is required for level more than 1.']})
        super().save(*args, **kwargs)    
    '''



    
class Filter(models.Model):
    name = models.CharField(unique=True, max_length=25, verbose_name='نام' if settings.ERROR_LANGUAGE=='pr' else 'name')                    
    slug = models.SlugField(allow_unicode=True, db_index=False, verbose_name='آدرس وب' if settings.ERROR_LANGUAGE=='pr' else 'slug')
    roots = models.ManyToManyField(Root, verbose_name='ريشه ها' if settings.ERROR_LANGUAGE=='pr' else 'roots')
    #filter_attributes

    class Meta:
        verbose_name = 'فيلتر' if settings.ERROR_LANGUAGE=='pr' else 'Filter'
        verbose_name_plural = 'فيلتر ها' if settings.ERROR_LANGUAGE=='pr' else 'Filters'
        
    def __str__(self):
        return str(self.name)




class Filter_Attribute(models.Model):
    name = models.CharField(max_length=25, verbose_name='نام' if settings.ERROR_LANGUAGE=='pr' else 'name') 
    filterr = models.ForeignKey(Filter, on_delete=models.CASCADE, related_name='filter_attributes', verbose_name='فيلتر' if settings.ERROR_LANGUAGE=='pr' else 'filter')                 #filter is reserved name by python

    class Meta:
        verbose_name = 'آيتم فيلتر' if settings.ERROR_LANGUAGE=='pr' else 'Filter Attribute'
        verbose_name_plural = 'آيتم هاي فيلتر' if settings.ERROR_LANGUAGE=='pr' else 'Filter Attributes'
        
    def __str__(self):
        return str(self.name)

        

        
class Rating(models.Model):                                                   #math operation of Rating will done in view. 
    submiters = models.PositiveIntegerField(default=0, verbose_name='وارد کنندگان' if settings.ERROR_LANGUAGE=='pr' else 'submiters')
    rate = models.DecimalField(max_digits=2, decimal_places=1, default=0, verbose_name='رتبه' if settings.ERROR_LANGUAGE=='pr' else 'rate')

    class Meta:
        verbose_name = 'رتبه بندي' if settings.ERROR_LANGUAGE=='pr' else 'Rating'
        verbose_name_plural = 'رتبه بندي ها' if settings.ERROR_LANGUAGE=='pr' else 'Ratings'
        
    def __str__(self):
        return str(self.rate)

    


def path_selector(instance, filename):
    return '{}_images/icons/%Y/%m/%d'.format(instance.path)

class Image_icone(models.Model):
    image = models.ImageField(upload_to=path_selector, verbose_name='تصوير' if settings.ERROR_LANGUAGE=='pr' else 'image')
    alt = models.CharField(max_length=55, blank=True, default='', verbose_name='توضيحات عکس' if settings.ERROR_LANGUAGE=='pr' else 'alt')
    path = models.CharField(max_length=20, default='products', verbose_name='آدرس' if settings.ERROR_LANGUAGE=='pr' else 'path')                  #can be value like: "products"  or  "posts" ....    

    class Meta:
        verbose_name = 'تصوير آيکن' if settings.ERROR_LANGUAGE=='pr' else 'Image icone'
        verbose_name_plural = 'تصاوير آيکن ها' if settings.ERROR_LANGUAGE=='pr' else 'Image icones'
        


    
class Post(models.Model):
    title = models.CharField(max_length=60, verbose_name='عنوان' if settings.ERROR_LANGUAGE=='pr' else 'title')
    slug = models.SlugField(allow_unicode=True, db_index=False, verbose_name='آدرس وب' if settings.ERROR_LANGUAGE=='pr' else 'slug')   #default db_index=True
    meta_title = models.CharField(max_length=60, blank=True, default='', verbose_name='متا عنوان' if settings.ERROR_LANGUAGE=='pr' else 'meta title')
    meta_description = models.TextField(validators=[MaxLengthValidator(160)], blank=True, default='', verbose_name='متا توضيحات' if settings.ERROR_LANGUAGE=='pr' else 'meta description')    
    brief_description = models.TextField(validators=[MaxLengthValidator(150)], verbose_name='توضيحات مختصر' if settings.ERROR_LANGUAGE=='pr' else 'brief description')
    visible = models.BooleanField(default=True, verbose_name='حذف' if settings.ERROR_LANGUAGE=='pr' else 'visible')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ انتشار' if settings.ERROR_LANGUAGE=='pr' else 'published date')
    image_icon = models.OneToOneField(Image_icone, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='تصوير آيکن' if settings.ERROR_LANGUAGE=='pr' else 'image icon')
    root = models.ForeignKey(Root, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='ريشه' if settings.ERROR_LANGUAGE=='pr' else 'root')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='نويسنده' if settings.ERROR_LANGUAGE=='pr' else 'author')
    #comment_set                                                   #backward relation
    #content_set
    
    class Meta:
        verbose_name = 'پست' if settings.ERROR_LANGUAGE=='pr' else 'Post'
        verbose_name_plural = 'پست ها' if settings.ERROR_LANGUAGE=='pr' else 'Posts'

    def __str__(self):
        represantaion = self.title[:20]+'...' if len(self.title) > 30 else self.title[:20]
        return represantaion

    


class ProductManager(models.Manager):                             #we have two seperate way for creating an object,  .create( product.objects.create ) and .save( p=product(..) p.save() ), it is important for us in two way rating creation suported same.
    def create(self, *args, **kwargs):
        product = super().create(*args, **kwargs)
        r = Rating.objects.create()
        product.rating = r
        product.save()
        return product

class Product(models.Model):                                     #.order_by('-available') shoud be done in views and in admin hasndy
    title = models.CharField(max_length=25, verbose_name='نام' if settings.ERROR_LANGUAGE=='pr' else 'title')
    slug = models.SlugField(allow_unicode=True, db_index=False, verbose_name='آدرس وب' if settings.ERROR_LANGUAGE=='pr' else 'slug')             #default db_index of slug is True
    meta_title = models.CharField(max_length=60, blank=True, default='', verbose_name='متا عنوان' if settings.ERROR_LANGUAGE=='pr' else 'meta title')
    meta_description = models.TextField(validators=[MaxLengthValidator(160)], blank=True, default='', verbose_name='متا توضيحات' if settings.ERROR_LANGUAGE=='pr' else 'meta description')
    brief_description = models.TextField(validators=[MaxLengthValidator(500)], verbose_name='توضيحات مختصر' if settings.ERROR_LANGUAGE=='pr' else 'brief description')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=-1, verbose_name='قيمت' if settings.ERROR_LANGUAGE=='pr' else 'price')
    available = models.BooleanField(default=False, db_index=True, verbose_name='موجودي' if settings.ERROR_LANGUAGE=='pr' else 'available')
    visible = models.BooleanField(default=True, verbose_name='حذف' if settings.ERROR_LANGUAGE=='pr' else 'delete')                #we use visible for deleting and object, for deleting visible=False, in fact we must dont delete any product.    
    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده' if settings.ERROR_LANGUAGE=='pr' else 'created')
    modified = models.DateTimeField(auto_now=True, verbose_name='تغيير يافته' if settings.ERROR_LANGUAGE=='pr' else 'modified')
    filter_attributes = models.ManyToManyField(Filter_Attribute, verbose_name='آيتم هاي فيلتر' if settings.ERROR_LANGUAGE=='pr' else 'Filter Attributes')
    root = models.ForeignKey(Root, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='ريشه' if settings.ERROR_LANGUAGE=='pr' else 'root')
    image_icon = models.OneToOneField(Image_icone, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='تصوير آيکن' if settings.ERROR_LANGUAGE=='pr' else 'image icon')     #in home page(page that list of product shown) dont query product.image_set.all()[0] for showing one image of product, instead query product.image_icone   (more fster)
    rating = models.OneToOneField(Rating, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='رتبه بندي' if settings.ERROR_LANGUAGE=='pr' else 'rating')
    #image_set                                                    backward relation field
    #comment_set

    objects = ProductManager()
        
    class Meta:
        verbose_name = 'کالا' if settings.ERROR_LANGUAGE=='pr' else 'Product'
        verbose_name_plural = 'کالا ها' if settings.ERROR_LANGUAGE=='pr' else 'Products'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        create_Rating = False
        if not self.pk:                                       #this condition will insure only creating product make rating creation(not in editing product). when you create new object like p = product(..)  p.save()   self.pk here is None
            create_Rating = True
        super().save(*args, **kwargs)
        if create_Rating:
            r = Rating.objects.create()
            self.rating = r
            self.save()


class Content(models.Model):
    text = models.TextField(verbose_name='متن' if settings.ERROR_LANGUAGE=='pr' else 'text')
    image = models.ImageField(upload_to='posts_images/%Y/%m/%d', blank=True, verbose_name='تصوير' if settings.ERROR_LANGUAGE=='pr' else 'image')
    video = models.FileField(upload_to='posts_videos/%Y/%m/%d', blank=True, verbose_name='ويديو' if settings.ERROR_LANGUAGE=='pr' else 'video')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست' if settings.ERROR_LANGUAGE=='pr' else 'Post')
    
    class Meta:                         #will not use here in production mode.
        verbose_name = 'محتوا' if settings.ERROR_LANGUAGE=='pr' else 'Content'
        verbose_name_plural = 'محتوا' if settings.ERROR_LANGUAGE=='pr' else 'Contents'

    def __str__(self):
        return str('محتواي {} مربوط به پست "{}"'.format(self.id, self.post))



    
class Image(models.Model):                                         
    image = models.ImageField(upload_to='products_images/%Y/%m/%d', verbose_name='تصوير' if settings.ERROR_LANGUAGE=='pr' else 'image')
    alt = models.CharField(max_length=55, blank=True, default='', verbose_name='توضيحات عکس' if settings.ERROR_LANGUAGE=='pr' else 'image alt')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا' if settings.ERROR_LANGUAGE=='pr' else 'product')
    
    class Meta:
        verbose_name = 'تصوير' if settings.ERROR_LANGUAGE=='pr' else 'Image'
        verbose_name_plural = 'تصاوير' if settings.ERROR_LANGUAGE=='pr' else 'Images'

        


class Comment(models.Model):
    confirm_status = models.CharField(max_length=1, verbose_name='وضعيت تاييد' if settings.ERROR_LANGUAGE=='pr' else 'confirm status')               #confirm site comments by admin and show comment in site if confirmed, '1' = confirmed     '2' = not checked(admin should check comment to confirm or not)      '3' = not confirmed(admin can confirm afters if want)    '4' = deleted
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ انتشار' if settings.ERROR_LANGUAGE=='pr' else 'published date')
    content = models.TextField(validators=[MaxLengthValidator(500)], verbose_name='محتوي' if settings.ERROR_LANGUAGE=='pr' else 'content')
    author = models.ForeignKey(User, related_name='comment_set_author', related_query_name='comments_author', on_delete=models.SET_NULL, null=True, blank=False, verbose_name='نويسنده' if settings.ERROR_LANGUAGE=='pr' else 'author')
    confermer = models.ForeignKey(User, related_name='comment_set_confermer', related_query_name='comments_confermer', on_delete=models.SET_NULL, null=True, blank=False, verbose_name='تاييد کننده' if settings.ERROR_LANGUAGE=='pr' else 'confermer')    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, verbose_name='پست' if settings.ERROR_LANGUAGE=='pr' else 'post')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, verbose_name='کالا' if settings.ERROR_LANGUAGE=='pr' else 'product')
    
    class Meta:
        verbose_name = 'نظر' if settings.ERROR_LANGUAGE=='pr' else 'Comment'
        verbose_name_plural = 'نظرات' if settings.ERROR_LANGUAGE=='pr' else 'Comments'


        

class Test3(models.Model):
    field_1 = models.CharField(max_length=60, unique=True, error_messages = {'unique': 'looooool', 'null': 'null loool'}, blank=False, null=False)


class Test4(models.Model):
    name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    available = models.BooleanField(error_messages = {'invalid': 'looooool', 'null': 'null loool'}, blank=False, null=False)

class Test5(models.Model):
    field_1 = models.GenericIPAddressField()
    field_2 = models.CharField(max_length=60, blank=True)

class Test6(models.Model):
    field_1 = models.CharField(verbose_name='فيلد 1', max_length=60, unique_for_date='created')
    created = models.DateTimeField()

#notes for video: why product.filter_filter_attribute should has 2 number? why filter.name unique but fulter_attribute.name not unique?
                 #wy post has not filter
    
