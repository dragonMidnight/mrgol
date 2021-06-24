from django.db.models import Max, Min

from .models import Product, Post



                           
def get_products(first_index, last_index):                                                                
    all_products_count = Product.objects.values_list('id').last()[0] - Product.objects.values_list('id').first()[0] + 1 #Product.objects.aggregate(product_counts=Max('id') - Min('id'))['product_counts'] + 1  #                    #.last run query like: SELECT "app1_product"."id"  FROM "app1_product"  ORDER BY "app1_product"."id" DESC  LIMIT 1               .first is like that but ASC instead of DESC       
    #instead up commend we have 2 way:  1- Product.objects.count()  that is heavy in running in huge amount of objects (tested in sqlite with 1.5m record)   2- #Product.objects.aggregate(product_counts=Max('id') - Min('id'))['product_counts']  this way  in performance is a bit more heavy than .last() and .first()  but use one query(.first .last use 2 query means connect 2 time to database), and also use MIN and MAX fun of database but .last .first use ORDER BY func of database (in sqlite ORDER BY is so fast maybe in another db be diffrent)  so .last .first is a bit faster but Max Min can be more logical.
    #we must havent eny id deleting in this project (and we havent)
    if all_products_count < last_index:
        return Product.objects.filter(visible=True).order_by('-available', '-id')
    else:                                                                                  #we have enough product in our db
        return Product.objects.filter(visible=True).order_by('-available', '-id')[first_index:last_index]        #dont have different beetwen Product.objects.filter(visible=True).order_by('-available', '-id')[first_index:last_index]   or    Product.objects.filter(id__in=list(range(first_index:last_index)), visible=True).order_by('-available', '-id')   they run same query in db.
    #we can use Product.objects.filter(id__in=ips, visible=True) but reverse is a bit faster(tested in sqlite with 1.5m record for retrive 100 object) it is more clear and breaf (dont need  list(range(min_ip, max_ip))) .....   and most important reason: reverse automaticly retrieve other objects if first objects havent our conditions(visible=True)  means if in Product.objects.filter(visible=True).reverse().order_by('id')[:5] we have two object with visible=False  in last 5 objects,  this commend will automaticly will go and retrive two other objects from next objects availabe. and if isnt find at all dont raise error and return founded objects,    query by indexed field(id) with an unindexed field (visible) dont affect speed significant(describe complete in:django/database.py/index)



            
def get_posts(first_index, last_index):                                   
    all_products_count = Post.objects.values_list('id').last()[0] - Post.objects.values_list('id').first()[0] + 1                    #.last run query like: #this line run this query: SELECT "app1_product"."id"  FROM "app1_product"  ORDER BY "app1_product"."id" DESC  LIMIT 1               .first is like that but ASC instead of DESC       
    #instead up commend we have 2 way:  1- Product.objects.count()  that is heave in huge amount of objects (tested in sqlite with 1.5m record)   2- #Product.objects.aggregate(product_counts=Max('id') - Min('id'))['product_counts']  this way  in performance is a bit more haveavy than .last() and .first()  but use one query(.first .last use 2 query means connect 2 time to database), and also use MIN and MAX fun of database but .last .first use ORDER BY func of database (in sqlite ORDER BY is so fast maybe in another db be diffrent)  so .last .first is a bit faster but Max Min can be more logical.
    if all_products_count < last_index:
        return Post.objects.filter(visible=True).order_by('-id')
    else:                                                                                  #we have enough product in our db
        return Post.objects.filter(visible=True).order_by('-id')[first_index:last_index] #we can use Product.objects.filter(id__in=ips, visible=True) but reverse is a bit faster(tested in sqlite with 1.5m record for retrive 100 object) is is more clear and breaf (dont need  list(range(min_ip, max_ip))) .....   and most important reason: reverse automaticly retrieve other objects if first objects havnt our conditions(visible=True)  means if in Product.objects.filter(visible=True).reverse().order_by('id')[:5] we have two object with visible=False  in last 5 objects,  this commend will automaticly will go and retrive two other objects from next objects availabe. and if isnt find at all dont raise error and return founded objects,    query by indexed field(id) with an unindexed field (visible) dont affect speed significant(describe complete in:django/database.py/index)



'''
children_root = []                        
def find_children_root(root):                    #root and all its chilidren will collect in children_root
    for child_root in Root.objects.filter(father_root_id=root.id):
        children_root += find_children_root(child_root)
    return root
'''



def childest_root(root):                    #root and all its children will collect in childs_and_root.  important: before calling childest_root must call get_childs_and_root.   why? childs_and_root must rest in every call if dont rest will collect its index in every refresh page.  
    for child_root in root.root_set.all():
        childs_and_root.append(childest_root(child_root))
    return root

def get_childs_and_root(root):                    #root and all its chilidren will collect in children_root
    global childs_and_root
    childs_and_root = []
    childest_root(root)
    return childs_and_root

def get_posts_products_by_roots(root):
    if root.level > 1:
        children_root_ids = [root.id for root in get_childs_and_root(root)]
    else:
        children_root_ids = [root.id]
    if root.post_product == 'product':
        return Product.objects.filter(root_id__in=children_root_ids)
    else:
        return Post.objects.filter(root_id__in=children_root_ids)        

            
class make_next:                             #for adding next to list you shold use iter like:  list_with_next = iter(L) but for using that you should call like: next(list_with_next) or list_with_next.__init__() and you cant next of use list_with_next in template like next(list_with_next) or list_with_next.__next__ or list_with_next.__init__() is error you must define simple method as def next(self) insinde list_with_next for using intemplate like: list_with_next.next
    def __init__(self, list):
        self.list = iter(list)
    def next(self):
        return next(self.list)




    
