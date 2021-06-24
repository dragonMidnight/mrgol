from django.contrib import admin
from django.urls import path
from django import forms
from django.db import models
from django.shortcuts import render
from django.http import QueryDict

import json

from . import myserializers
from . import myforms
from .models import Test3, Root, Filter, Filter_Attribute, Content, Post, Rating, Product, Image, Image_icone, Comment




class CommentInline(admin.StackedInline):
    model = Comment
    fields = ('author', 'confermer', 'confirm_status', 'published_date', 'content')
    readonly_fields = ('author', 'confermer', 'confirm_status', 'published_date', 'content')

class PostAdmin(admin.ModelAdmin):
    #filter_horizontal = ('contents',)
    prepopulated_fields = {'slug':('title',)}
    inlines = [CommentInline]
    readonly_fields = ('published_date',)
admin.site.register(Post, PostAdmin)




from django.conf import settings
from .mywidgets import filter_attributes_widget, root_widget
from .myfields import CustomChoiceField
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    inlines = [CommentInline]
    readonly_fields = ('rating',)
    form = myforms.ProductForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST':
            filter_attributes_value = []
            for i in range(1, 50):
                filter_attribute_name = 'filter_attributes'+str(i)
                filter_attribute_value = request.POST.get(filter_attribute_name)
                if filter_attribute_value:
                    filter_attributes_value += filter_attribute_value
            post = request.POST.copy()
            post.setlist('filter_attributes', filter_attributes_value)
            request.POST = post
        return super().change_view(request, object_id, form_url, extra_context)
    
    '''
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST':
            return super().change_view(request, object_id, form_url, extra_context)
        
        else:
            current_product = Product.objects.get(id=object_id)
            roots_id_str = [(root.id, root.__str__()) for root in Root.objects.filter(post_product='product')]
            filters = Filter.objects.all()
            filters_attributes = []
            for filter in filters:                 #in this part we want create dynamicly options inside <select ..> </select>  for field root.level depend on validators we define in PositiveSmallIntegerField(validators=[here]) for example if we have MinValueValidator(1) MaxValueValidator(3) we have 3 options: <option value="1"> 1 </option>   <option value="2"> 2 </option>   <option value="3"> 3 </option>                   
                filters_attributes += [json.dumps([serializer for serializer in myserializers.Filter_AttributeListSerializer(filter.filter_attributes.all(), many=True).data])]

            selected_filters_attributes = current_product.filter_attributes.all()
            selected_filters_attributes_ids = [filter_attribute.id for filter_attribute in selected_filters_attributes]
            selected_filters_ids = [filter_attribute.filterr.id for filter_attribute in selected_filters_attributes]
            return render(request, 'admin/change_product_template.html', {
                'current_product': current_product,
                'selected_filters_attributes': selected_filters_attributes,
                'selected_filters_attributes_ids': selected_filters_attributes_ids,
                'selected_filters_ids': selected_filters_ids,
                'filters_filters_attributes': list(zip(filters, filters_attributes)),
                'range_1': '1:{}'.format(len(filters)),
                'roots_id_str': roots_id_str})
    '''
admin.site.register(Product, ProductAdmin)




class CommentAdmin(admin.ModelAdmin):
    pass
    #readonly_fields = ('author', 'confermer', 'published_date', 'post', 'product')
admin.site.register(Comment, CommentAdmin)




Root_level_CHOICES = ((1,'1'), (2,'2'), (3,'3'))               #value for send is first element (here like 1) and value for showing is second (here like '1')
class RootAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    formfield_overrides = {models.PositiveSmallIntegerField: {'widget': forms.Select(choices=Root_level_CHOICES)}}
    '''
    def get_urls(self):
        urls = super().get_urls()
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)
        info = self.model._meta.app_label, self.model._meta.model_name

        for i in range(len(urls)):
            try:                                  #some urls have not .pattern so raise error in if istatment without try.
                if '/change/' in str(urls[i].pattern):
                    urls[i] = path('<path:object_id>/change/', wrap(self.change_view), name='%s_%s_change' % info)
            except:
                pass
   
        my_urls = [path('aa/', self.my_view)]            
        return my_urls + urls
    
    def my_view(self, request):
        return render(request, 'change.html', {})#HttpResponse('loooooooooooooooooool')
    '''
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST':
            return super().change_view(request, object_id, form_url, extra_context)            
        
        else:
            root = Root.objects.get(id=object_id)
            for field in root._meta.fields:                 #in this part we want create dynamicly options inside <select ..> </select>  for field root.level depend on validators we define in PositiveSmallIntegerField(validators=[here]) for example if we have MinValueValidator(1) MaxValueValidator(3) we have 3 options: <option value="1"> 1 </option>   <option value="2"> 2 </option>   <option value="3"> 3 </option>                   
                if isinstance(field, models.PositiveSmallIntegerField):
                    level_field = field                                  #optain object PositiveSmallIntegerField of Root.level, note: root.level is not same with level_field (root.level.validators raise error) root.level is field value and some limited attributes and level_field is object PositiveSmallIntegerField created by root.level with full attrs of PositiveSmallIntegerField like validators (validators we definded in PositiveSmallIntegerFieldand argument and...)      
            limit_value_MinValueValidator, limit_value_MaxValueValidator = level_field.validators[0].limit_value,  level_field.validators[1].limit_value
            MinValue_MaxValue_range = list(range(limit_value_MinValueValidator, limit_value_MaxValueValidator+1))   #limit_value_MinValueValidator here is 1 because in validators we definded MinValueValidator(1)  and limit_value_MaxValueValidator here is 3 because we definded MaxValueValidator(3)   
            
            roots_seperated_by_level_jslist = []
            all_roots = Root.objects.all()
            for i in MinValue_MaxValue_range:
                roots_seperated_by_level_jslist += [json.dumps([serializer for serializer in myserializers.RootListSerializer(all_roots, many=True).data if serializer['level']==i-1])]           #1- we dont need other fields of root (so just use __str())   2- json.dumps is in fact aray of javascript, because python list can use as javascript aray. supose: L=[1,2,3],  L cant use in javascript as list(javascript dont understand that) but in js_L=json.dumps(L) we can use js_L in javascript ez.   3- we cant use list in list in json.dumps() for example json.dumps([[1,2], [3,4]]) isnt acceptable.                  
            return render(request, 'admin/change_root_template.html', {
                'root': root,
                'levelrange_roots': list(zip(MinValue_MaxValue_range, roots_seperated_by_level_jslist)),
                'range_1': '1:{}'.format(MinValue_MaxValue_range[-1])})      #why we used range_1?  because in django template we cant refere to last index by this way: L[1:]  so this is error: {% for i, j in levelrange_roots|slice:"1:" %}  so we need find last index here and send to template (like "1:3" that 3 is last index) but note using {{ }} will make work in django template like: {{ for i, j in levelrange_roots|slice:"1:" }}    this is work without eny error(i dont know why)




class FilterAdmin(admin.ModelAdmin):
    filter_horizontal = ('roots',)
    prepopulated_fields = {'slug':('name',)}
        
admin.site.register(Filter, FilterAdmin)




admin.site.register(Content)
admin.site.register(Rating)
admin.site.register(Image)
admin.site.register(Image_icone)
admin.site.register(Test3)
admin.site.register(Filter_Attribute)    
admin.site.register(Root, RootAdmin)

#admin.site.disable_action('delete_selected') 

