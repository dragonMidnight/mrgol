from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextInputWidget

import json

from . import myserializers
from .models import Product, Root, Filter, Filter_Attribute
from .mymethods import make_next



    
class filter_attributes_widget(forms.Select):
    template_name = 'app1/fomrs_widgets/filter_attributes_two_select.html'
    
    def get_context(self, name, value, attrs):
        two_select_context = super().get_context(name, value, attrs)

        filters = list(Filter.objects.prefetch_related('filter_attributes'))               #if dont use list, using filters again, reevaluate filters and query again to database!
        filters_attributes = []
        for filter in filters:                 #in this part we want create dynamicly options inside <select ..> </select>  for field root.level depend on validators we define in PositiveSmallIntegerField(validators=[here]) for example if we have MinValueValidator(1) MaxValueValidator(3) we have 3 options: <option value="1"> 1 </option>   <option value="2"> 2 </option>   <option value="3"> 3 </option>                   
            filters_attributes += [json.dumps([serializer for serializer in myserializers.Filter_AttributeListSerializer(filter.filter_attributes.all(), many=True).data])]
        two_select_context['filters_filters_attributes'] = list(zip(filters, filters_attributes))
        two_select_context['range_filters'] = '1:{}'.format(len(filters))
        two_select_context['selected_filter_attributes_ids'] = []
        two_select_context['selected_filters_ids'] = []

        if value.id:
            selected_filter_attributes = value.filter_attributes.select_related('filterr')      #value is current product.  
            selected_filters = [filter_attribute.filterr for filter_attribute in selected_filter_attributes if filter_attribute]             #if value.filter_attributes.all() was blank, filter_attribute.id  raise error so we need check with if filter_attribute
            selectname_filters, selectid_filters, selectname_filter_attributes, selectid_filter_attributes = [], [], [], []
            for i in range(1, len(selected_filters)):
                selectname_filters += ['filters'+str(i+1)]
                selectid_filters += ['id_filters'+str(i+1)]
                selectname_filter_attributes += ['filter_attributes'+str(i+1)]
                selectid_filter_attributes += ['id_filter_attributes'+str(i+1)]
            two_select_context['selected_filter_attributes'] = make_next(selected_filter_attributes)  
            two_select_context['selected_filters'] = make_next(selected_filters)
            two_select_context['selectname_filters'], two_select_context['selectid_filters'] = make_next(selectname_filters), make_next(selectid_filters)
            two_select_context['selectname_filter_attributes'], two_select_context['selectid_filter_attributes'] = make_next(selectname_filter_attributes), make_next(selectid_filter_attributes)
        return two_select_context




class root_widget(forms.Select):
    template_name = 'app1/fomrs_widgets/root_two_select.html'
    
    def get_context(self, name, value, attrs):
        two_select_context = super().get_context(name, value, attrs)

        roots = list(Root.objects.all())
        roots_level_range = list(range(roots[0].level, roots[-1].level+1))
        roots_by_level = []
        for i in roots_level_range:
            same_level_roots = []
            for root in roots:                             
                if root.level == i:
                    same_level_roots += [root]
            roots_by_level += [same_level_roots]
        rootsbyleveljs_levels = []
        for same_roots in roots_by_level:
            rootsbyleveljs_levels += [[json.dumps([serializer for serializer in myserializers.RootListSerializer(same_roots, many=True).data]), same_roots[0].level]]
        two_select_context['roots_level_range'] = roots_level_range
        two_select_context['rootsbyleveljs_levels'] = rootsbyleveljs_levels
        two_select_context['range_1'] = '1:{}'.format(len(rootsbyleveljs_levels))
        two_select_context['selected_level_range'] = -1
        two_select_context['selected_root_id'] = -1
            
        if value.id:
            two_select_context['selected_level_range'] = value.root.level
            two_select_context['selected_root_id'] = value.root.id
            
        return two_select_context
