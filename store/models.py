from django.db import models
import datetime
#Create your models here.

class Product_Category(models.Model):
    Category_Name = models.CharField(max_length = 100)


    def __str__(self):
        return self.Category_Name

class Product_Selling_Category(models.Model):
    Selling_Category_Name = models.CharField(max_length = 100)


    def __str__(self):
        return self.Selling_Category_Name

class Product_Details(models.Model):
    Product_ID = models.CharField(max_length = 50, primary_key = True)
    Product_Image1 = models.ImageField(upload_to = "img/%y")
    Product_Image2 = models.ImageField(upload_to = "img/%y")
    Product_Title = models.CharField(max_length=200)
    Product_Category = models.ForeignKey(Product_Category, on_delete=models.CASCADE)
    Product_Selling_Category = models.ForeignKey(Product_Selling_Category, on_delete=models.CASCADE, blank = True, null = True)
    Product_Description = models.TextField()
    Product_Price = models.DecimalField(max_digits = 10,decimal_places = 2)


    def __str__(self):
        return self.Product_Title

class Website_Info(models.Model):
    Email = models.CharField(max_length=50)
    Contact = models.CharField(max_length=30)
    Address = models.CharField(max_length=50)
    Store_Timings = models.CharField(max_length=100)
    Facebook = models.CharField(max_length=50)
    Instagram = models.CharField(max_length=50)
    Twitter = models.CharField(max_length=50)

class User_Details(models.Model):
    User_ID = models.AutoField(primary_key = True)
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Image = models.ImageField(upload_to = "userimages", default="default.png", null =True, blank = True)
    Email = models.EmailField(max_length=100)
    Contact = models.IntegerField()
    Address = models.TextField()
    Password = models.CharField(max_length=30)

    def __str__(self):
        return self.Email


    def isexist(self):
        if User_Details.objects.filter(Email = self.Email):
            return True

        return False


class About_Us(models.Model):
    About_Section_Title = models.CharField(max_length=100)
    Description = models.TextField()

class Pictures_Gallery(models.Model):
    ID = models.AutoField(primary_key = True)
    Image = models.ImageField(upload_to = "img/%y")
   

class Orders(models.Model):
    Order_ID = models.AutoField(primary_key = True)
    Delivered = models.BooleanField(default = False)

    def __str__(self):
        return str(self.Order_ID)


class Order_Request(models.Model):
    Order_ID = models.ForeignKey(Orders, on_delete = models.CASCADE)
    Product_Title = models.ForeignKey(Product_Details, on_delete = models.CASCADE)
    Quantity = models.IntegerField(default = 1)
    Price = models.IntegerField()
    Customer = models.ForeignKey(User_Details, on_delete = models.CASCADE)
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Phone = models.CharField(max_length = 11)
    Address = models.TextField()
    City = models.CharField(max_length=50)
    Province = models.CharField(max_length=50)
    District = models.CharField(max_length=50)
    Zip_Code = models.CharField(max_length=50)
    Date = models.DateField(default = datetime.datetime.today)


    def __str__(self):
        return str(self.Order_ID)
        

