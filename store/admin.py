from django.contrib import admin
from .models import *
# Register your models here.

class productcategory_data(admin.ModelAdmin):
    list_display = ['Category_Name']

class productsellingcategory_data(admin.ModelAdmin):
    list_display = ['Selling_Category_Name']

class productdetails_data(admin.ModelAdmin):
    list_display = ['Product_ID','Product_Image1','Product_Image2','Product_Title','Product_Category','Product_Selling_Category','Product_Description','Product_Price']

class website_information_Data(admin.ModelAdmin):
    list_display = ['Email','Contact','Address','Store_Timings','Facebook','Instagram','Twitter']

class user_details_data(admin.ModelAdmin):
    list_display = ['User_ID','First_Name','Last_Name','Email','Contact','Password']

class aboutus_data(admin.ModelAdmin):
    list_display = ['About_Section_Title', 'Description']

class pictursgallery_data(admin.ModelAdmin):
    list_display = ['ID','Image']

class orders_data(admin.ModelAdmin):
    list_display = ['Order_ID','Customer','Product','Quantity','Price','Date', 'Delivered']

admin.site.register(Product_Category,productcategory_data)
admin.site.register(Product_Selling_Category,productsellingcategory_data)
admin.site.register(Product_Details, productdetails_data)
admin.site.register(Website_Info, website_information_Data)
admin.site.register(User_Details, user_details_data)
admin.site.register(About_Us, aboutus_data)
admin.site.register(Pictures_Gallery, pictursgallery_data)
# admin.site.register(Orders)
# # admin.site.register(orderl)
admin.site.register(Order_Request)

class orderItemInline(admin.TabularInline):
    model = Order_Request
    # raw_id_fields =['Order_ID']

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['Order_ID']
    inlines = [orderItemInline]


