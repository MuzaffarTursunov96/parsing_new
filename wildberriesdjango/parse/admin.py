# from django.contrib import admin
#
# # Register your models here.
# from .models import *
#
# # @admin.register(Branches)
# # class ProductAdmin(admin.ModelAdmin):
# #     list_display = ['name', 'created_at', 'updated_at', ]
#
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id','name', 'created_at', 'updated_at' ]
#     readonly_fields = ('id',)
#
# admin.site.register(Branches, ProductAdmin)
#
# @admin.register(Attributes)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'branch_id', 'name','combination','created_at','updated_at','deleted_at' ]
#
# @admin.register(Characteristics)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'attribute_id', 'name','slug','created_at','updated_at','deleted_at' ]
#
# @admin.register(Categories)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id','parent_id', 'level', 'name','order_level','commision_rate','banner','icon','featured','top','digital','slug','meta_title','meta_description','created_at','updated_at','field_lft','field_rgt','deleted_at' ]
#     readonly_fields = ('id',)
#
# @admin.register(AttributeCategory)
# class ProductAttr(admin.ModelAdmin):
#     list_display = ['id','attribute_id','category_id']
#
# @admin.register(Brands)
# class ProductAttr(admin.ModelAdmin):
#     list_display = ['id','name','logo','top','slug','meta_title','meta_description','created_at','updated_at']
#
# @admin.register(Uploads)
# class ProductAttr(admin.ModelAdmin):
#     list_display = ['id','file_original_name','file_name','user_id','file_size','extension','type','created_at','updated_at','deleted_at']
#
# @admin.register(Colors)
# class ProductAttr(admin.ModelAdmin):
#     list_display = ['id','name','code','created_at','updated_at']
#
# @admin.register(Elements)
# class ProductAttr(admin.ModelAdmin):
#     list_display = ['id','name','added_by','user_id','category_id','parent_id','brand_id','photos','thumbnail_img','video_provider','video_link','tags','description','characteristics',
#                     'variations','variation_attributes','variation_colors','todays_deal','published','featured','unit','weight','num_of_sale','meta_title','meta_description',
#                     'meta_img','pdf','slug','earn_point','rating','barcode','digital','file_name','file_path','created_at','updated_at','deleted_at','on_moderation','is_accepted','refundable'
#                     ]
#
#
# @admin.register(Variations)
# class ProductAttr(admin.ModelAdmin):
#     list_display = ['id','name','lowest_price_id','slug','partnum','element_id','prices','variant','created_at','updated_at','user_id','num_of_sale','qty','rating','thumbnail_img','photos','color_id','characteristics','deleted_at']
# @admin.register(Languages)
# class ProductAttr(admin.ModelAdmin):
#     list_display = ['id','name','code','rtl','created_at','updated_at']
#
