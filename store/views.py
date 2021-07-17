from django.views.generic.base import TemplateResponseMixin
from store.templatetags.cart import price_total
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from store.auth import auth_middleware
from django.template.loader import get_template
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .forms import *
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template, RequestContext, context
from io import BytesIO
from datetime import datetime
x = datetime.now
# Create your views here.

def insert(request):
    form = testingform()
    if request.method == 'POST':
        form = testingform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
        
    return render(request, 'edit.html', context)

def deldata(request, pk):
    em = Website_Info.objects.get(Email = pk)
    em.delete()
    return redirect('/')

def update(request, pk):
    em = Website_Info.objects.get(Email = pk)
    form = testingform(instance = em)

    if request.method == 'POST':
        form = testingform(request.POST, instance = em )
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
        
    return render(request, 'edit.html', context)

def p_details(request, pk):
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    pr = Product_Details.objects.get(Product_ID = pk)
    # print(pr)
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1 
        request.session['cart'] = cart
        print('cart : ',request.session['cart'])
        return redirect('p_details', pk)
    context = {
        'prd': pr,
        'pr':products,
    }

    return render(request, 'product_details.html', context)

def index(request):
    # user = request.session.get('user')
    crt = request.session.get('cart')
    # print(crt)
    if not crt:
        request.session['cart'] = {}
    web_info = Website_Info.objects.all()
    pictures_gallery = Pictures_Gallery.objects.all()
    popular_items = Product_Details.objects.filter(Product_Selling_Category__Selling_Category_Name='Popular Items')
    new_arrival = Product_Details.objects.filter(Product_Selling_Category__Selling_Category_Name='New Arrivals')
    home_slider = Product_Details.objects.filter(Product_Selling_Category__Selling_Category_Name='Home Slider')
    watch_of_choice = Product_Details.objects.filter(Product_Selling_Category__Selling_Category_Name='Watch of Choice')
    # print(product_details)
    
    ids = list(request.session.get('cart').keys())  
    
    # print(ids)
    products = Product_Details.objects.filter(Product_ID__in = ids)
    wi = {
        'wi': web_info,
        'pi': popular_items,
        'na': new_arrival,
        'hs': home_slider,
        'pg': pictures_gallery,
        'woc': watch_of_choice,
        'pr': products,
    }
    # print(request.session.get('user_id'))
    # print(request.session.get('user'))
    print(request.session.get('email'))
    return render(request, 'index.html', wi )

def about(request):
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    web_info = Website_Info.objects.all()
    about = About_Us.objects.all()
    wi = {
        'wi': web_info,
        'about': about,
        'pr': products
    }
    return render(request, 'about.html', wi )

def cart(request):
    print(request.session['cart'])
    if request.method == 'POST':
        product = request.POST.get('product')
        cart = request.session.get('cart')
        # print(cart)
        if cart:
            quantity = cart.get(product)
            print(cart)
            if quantity:
                cart.pop(product)

        request.session['cart'] = cart
        # print('cart : ',request.session['cart'])
        return redirect('cart')
        # request.session['cart'] = cart
        # # print('cart : ',request.session['cart'])
        # return redirect('cart')
    user = request.session.get('user')
    # print(user)
    ids = list(request.session.get('cart').keys())  
    
    # print(ids)
    products = Product_Details.objects.filter(Product_ID__in = ids)
    # if ids == 'None':
    #     request.session['cart'] = {}
    # if cart:
    #     quantity = cart.get(product)
    
    web_info = Website_Info.objects.all()
    wi = {'wi': web_info,
        'pr': products
    }
    return render(request, 'cart.html', wi )

def orders(request):
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    if request.method == 'GET':
        user = request.session.get('user')
        # print(user)
        orders = Order_Request.objects.filter(Customer= user).order_by('-Date')
        # print(deliverd.Delivered)
        # orders = orders.reverse()
        # print(deliverd)
        context = {
            'orders': orders,
            'pr': products,
        }
        return render(request, 'orders.html', context)

def checkout(request):
    wi = Website_Info.objects.all()
    if request.method == 'POST':
        ab = request.session['cart']
        Orders.objects.create()
        max_val = Orders.objects.latest('Order_ID')
        cart = request.session.get('cart')
        print(cart)
        customer = request.session.get('user')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('contact')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        distt = request.POST.get('distt')
        zip_code = request.POST.get('zip')
        cart = request.session.get('cart')
        ids = list(request.session.get('cart').keys())
        products = Product_Details.objects.filter(Product_ID__in = ids)
        amount = 0
        tempamount = 0
        total = 0
        quantity = []
        # print(products)
        for items in products:
            Order_Request.objects.create(Order_ID = max_val,
            Product_Title = items, 
            Quantity = cart.get(str(items.Product_ID)), 
            Price = items.Product_Price,
            Customer = User_Details(User_ID = customer), 
            First_Name = request.POST.get('fname'),
            Last_Name = request.POST.get('lname'),
            Address = address,
            Phone = phone,
            City = city,
            Province = province,
            District = distt,
            Zip_Code = zip_code,
            )
            tempamount = (items.Product_Price * cart.get(str(items.Product_ID)))
            amount += tempamount
            quantity = cart.get(str(items.Product_ID))
        total = amount

        # amount = 0
        # tempamount = 0
        # total = 0
        # quantity = []
        # for items in products:
        #     tempamount = (items.Product_Price * cart.get(str(items.Product_ID)))
        #     amount += tempamount
        #     quantity.insert(len(quantity),cart.get(str(items.Product_ID)))
        # total = amount

        # context = {'pr':products, 'total': total, 'qty': quantity}
        # msg_plain = render_to_string('email.txt')
        # msg_html = render_to_string('email.html',context)
        # recipient = (request.session.get('email'))
        # send_mail("Your order has been placed", msg_plain, settings.EMAIL_HOST_USER,
        #             [recipient], html_message = msg_html)
        # request.session['cart'] = {}

        user = request.session.get('user')
        # print(user)
        # orders = Order_Request.objects.filter(Customer = user).order_by('-Date')
        # orders = orders.reverse()
        # print(orders)


        # cart = request.session.get('cart')
        # ids = list(request.session.get('cart').keys())
        # products = Product_Details.objects.filter(Product_ID__in = ids)
        # amount = 0
        # tempamount = 0
        # total = 0
        # quantity = []
        # for items in products:
        #     tempamount = (items.Product_Price * cart.get(str(items.Product_ID)))
        #     amount += tempamount
        #     quantity.insert(len(quantity),cart.get(str(items.Product_ID)))
        # total = amount
        # data = {'pr': products, 'wi':wi, 'total': total, 'qty': quantity, 'time': x}
        # template = get_template("invoice.html")
        # data_p = template.render(data)
        # response = BytesIO()
        # pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)
        # if not pdfPage.err:
        #     return HttpResponse(response.getvalue(), content_type = "application/pdf")
            
        # else:
        #     return HttpResponse("Error")
        
        
            

            
            # context = {
            #     'pr':products,
            # }
            # message = get_template('email.html', context, context_instance=RequestContext(request))
            # recipient = (request.session.get('email'))
            # msg = EmailMessage(
            #     'Subject',
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     ['uzair8489@gmail.com'],
            #     )
            # msg.content_subtype = "html"  # Main content is now text/html
            # msg.send()

            # request.session['cart'] = {}
        # return redirect('shop')
        # customer = request.session.get('user')
        # fname = request.POST.get('fname')
        # lname = request.POST.get('lname')
        # phone = request.POST.get('contact')
        # address = request.POST.get('address')
        # city = request.POST.get('city')
        # province = request.POST.get('province')
        # distt = request.POST.get('distt')
        # zip_code = request.POST.get('zip')
        # cart = request.session.get('cart')
        # ids = list(request.session.get('cart').keys())
        # products = Product_Details.objects.filter(Product_ID__in = ids)
        # # prod = list(Product_Details.objects.filter(Product_Title__in = products))
        # # print(products)
        # # print(prod)
        # # print(address, phone, customer, cart, products)
        # for items in products:
        #     order = Orders(Customer = User_Details(User_ID = customer), 
        #     First_Name = fname,
        #     Last_Name = lname,
        #     Product = items,
        #     Quantity = cart.get(str(items.Product_ID)),
        #     Price =  items.Product_Price, 
        #     Address = address,
        #     Phone = phone,
        #     City = city,
        #     Province = province,
        #     District = distt,
        #     Zip_Code = zip_code,
        #     )
        #     # print(order)
        #     order.save()
        
    # message = 'Product: '+str(products) + 'Price:'+ str(products.Product_Price)
    # subject = 'Code Band'
    # message = str(products)
    # sender = 'estore479@gmail.com'
    # recipient = (request.session.get('email'))

    # send_mail(
    #     subject,
    #     message,
    #     sender,
    #     [recipient]
    #     )
    return redirect('confirmation')

def confirmation(request):
    ids = list(request.session.get('cart').keys())
    products = Product_Details.objects.filter(Product_ID__in = ids)
    web_info = Website_Info.objects.all()
    wi = {'wi': web_info, 'pr': products
    }
    return render(request, 'confirmation.html', wi )

def contact(request):
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    web_info = Website_Info.objects.all()
    # contact = Contact_Us.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact = Contact_Us(Name = name, Email = email, Message = message)
        contact.save()
        msg_plain = render_to_string('email.txt')
        msg_html = render_to_string('thankyou.html')
        recipient = request.POST.get('email')
        send_mail("Thank you for contacting us", msg_plain, settings.EMAIL_HOST_USER,
                    [recipient], html_message = msg_html)

        subject = 'Message Received from ' + email 
        message = request.POST.get('message')
        sender = settings.EMAIL_HOST_USER
        recipient = (settings.EMAIL_HOST_USER)

        send_mail(
            subject,
            message,
            sender,
            [recipient]
        )
    pname = request.POST.get('name')
    wi = {'wi': web_info,
          'pr': products,
          'pname': pname,
    }
    return render(request, 'contact.html', wi )

def elements(request):
    web_info = Website_Info.objects.all()
    wi = {'wi': web_info,
    }
    return render(request, 'elements.html', wi )

def main(request):
    web_info = Website_Info.objects.all()
    wi = {'wi': web_info,
    }
    return render(request, 'main.html', wi )

def product_details(request):
    web_info = Website_Info.objects.all()
    wi = {'wi': web_info,
    }
    return render(request, 'product_details.html' )

def shop(request):
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    product_details = Product_Details.objects.all()
    web_info = Website_Info.objects.all()
    product_category = Product_Category.objects.all()
    if request.method == 'POST':
        product = request.POST.get('product')
        # ptitle = request.POST.get('product-title')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1 
        request.session['cart'] = cart
        # print('cart : ',request.session['cart'])
        return redirect('shop')

    category = request.GET.get('category')
    product_details = None  
    if category:
        product_details = Product_Details.objects.filter(Product_Category = category)
    else:
        product_details = Product_Details.objects.all()
        
        web_info = Website_Info.objects.all()
    
        product_category = Product_Category.objects.all()


    ids = list(request.session.get('cart').keys())  
    
    # print(ids)
    products = Product_Details.objects.filter(Product_ID__in = ids)
    
    pd = {
        'prd':product_details,
        'wi': web_info,
        'pc': product_category,
        'pr': products
        } 
    return render(request, 'shop.html', pd)

def handlesignup(request):
    if request.method == 'POST':
        #Get the post parameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('index')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('index')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('index')

        # check for errorneous inputs

        #create user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname            
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your Account Has Been Created Successfully')
        return redirect('/')

    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        #Get the post parameter
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username = loginusername, password = loginpass)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "invalid Credentials, Please try again")
            return redirect('index')

    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'GET':

        return render(request, 'signup.html')
    else:
        #Get the post parameter
        postData = request.POST
        fname = postData.get('fname')
        lname = postData.get('lname')
        email = postData.get('email')
        contact = postData.get('contact')
        pass1 = postData.get('pass1')
        pass2 = postData.get('pass2')

        value = {
            'fname' : fname,
            'lname' : lname,
            'email' : email,
            'contact' : contact,
        }

        error_message = None

        signup = User_Details(First_Name = fname, Last_Name = lname, Email = email,Contact = contact, Password = pass1)

        # print(fname, lname)
        if pass1 != pass2:
            error_message = 'Password does not match'

        if len(contact) < 11:
            error_message = 'Phone number should be 11 digits long'
        
        if len(contact)> 11:
            error_message = 'Phone number must not be greater than 11 digits'

        if len(pass1) < 6:
            error_message = 'Password must be 6 characters long'

        if signup.isexist():
            error_message = 'Email Address Already Exists'

        if not error_message:
            signup.save()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value,
            }
            return render(request, 'signup.html', data)

def login(request):
    wi = Website_Info.objects.all()
    ids = list(request.session.get('cart').keys())
    
    # print(ids)
    products = Product_Details.objects.filter(Product_ID__in = ids)
    if request.method == 'GET':
        # request.session['cart'] = {}
        
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        user = User_Details.objects.filter(Email = email)
        u_pass = User_Details.objects.filter(Password = password)
        
        value = {
            'email': email
        }
        error_message = None
        if user:
            if u_pass:
                userid = User_Details.objects.get(Email = email)
                request.session['user'] = userid.User_ID
                request.session['fname'] = userid.First_Name
                request.session['lname'] = userid.Last_Name
                request.session['email'] = userid.Email

                # data = {
                #     'values': value,
                #     'error': error_message,
                #     'pr': products
                # }

                return redirect('index')
            elif not u_pass:
                error_message = 'Invalid Email or password'
                data = {
                    'values': value,
                    'error': error_message,
                    'pr': products,
                    'wi': wi
                }
        else:
            error_message = 'User does not exists'
            data = {
                'values': value,
                'error': error_message,
                'pr': products,
                'wi': wi
            }
        # print(email)
        return render(request, 'login.html', data)

def logout(request):    
    request.session.clear()
    request.session['cart'] = {}
    return redirect('login')

def pdfinvoice(request):
    amount = 0
    tempamount = 0
    total = 0
    qty = 0
    cart = request.session.get('cart')
    wi = Website_Info.objects.all()
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    for items in products:
        tempamount = (items.Product_Price * cart.get(str(items.Product_ID)))
        amount += tempamount
    total = amount
    if request.method == 'GET':
        user = request.session.get('user')
        orders = Order_Request.objects.filter(Customer = user).order_by('-Date')
        # orders = orders.reverse()
        # print(orders)
        context = {
            'orders': orders,
            'total': total,
        }
    return render(request, 'invoicePdfReport.html', context)

def create_invoice(request):
    wi = Website_Info.objects.all()
    amount = 0
    tempamount = 0
    total = 0
    quantity = []
    cart = request.session.get('cart')
    wi = Website_Info.objects.all()
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    for items in products:
        tempamount = (items.Product_Price * cart.get(str(items.Product_ID)))
        amount += tempamount
        quantity.insert(len(quantity),cart.get(str(items.Product_ID)))
    total = amount
    if request.method == 'GET':
        user = request.session.get('user')
        # print(user)
        # orders = Order_Request.objects.filter(Customer = user).order_by('-Date')
        # orders = orders.reverse()
        # print(orders)
        data = {'pr': products, 'wi':wi, 'total': total, 'qty': quantity, 'time': x}
        template = get_template("invoice.html")
        data_p = template.render(data)
        response = BytesIO()
        pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)
        if not pdfPage.err:
            request.session['cart'] ={}
            return HttpResponse(response.getvalue(), content_type = "application/pdf")
            
        else:
            return HttpResponse("Error")
    
        # response = HttpResponse(content_type = 'application/pdf')
        # response['Content-Dispositon'] = 'filename = "OrderInvoice.pdf"'
        # template = get_template(template_path)
        # html = template.render(context)

        # #create a pdf
        # pisa_status = pisa.CreatePDF(html, dest =response)
        # # if error then show this
        # if pisa_status.err:
        #     return HttpResponse('We had error <pre>' + html + '</pre>')
        # return response

def userprofile(request, pk):
    # pk = request.session.get('user')
    userid = User_Details.objects.get(User_ID = pk)
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    if request.method == 'POST':
        userid.First_Name = request.POST.get('fname')
        userid.Last_Name = request.POST.get('lname')
        userid.Email = request.POST.get('email')
        userid.Contact = request.POST.get('contact')
        userid.Address = request.POST.get('address')
        userid.Image = request.FILES.get('img')
        # print(userimg)
        # messages.success(request, 'Your Account Has Been Created Successfully')
        userid.save()
        return redirect('userprofile', pk)
        
    context = {
        'userid': userid,
        'pr': products
    }
        
    return render(request, 'userprofile.html', context)

def check(request):
    wi = Website_Info.objects.all()
    ids = list(request.session.get('cart').keys())
    products = Product_Details.objects.filter(Product_ID__in = ids)

    context = {
        'wi': wi,
        'pr':products,
    }
    return render(request, 'checkout.html', context)

def ordemail(request):
    amount = 0
    tempamount = 0
    total = 0
    quantity = []
    cart = request.session.get('cart')
    wi = Website_Info.objects.all()
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    for items in products:
        tempamount = (items.Product_Price * cart.get(str(items.Product_ID)))
        amount += tempamount
        quantity.insert(len(quantity),cart.get(str(items.Product_ID)))
    total = amount
    context = {
        'pr':products,
        'total': total,
        'qty': quantity,
    }
    return render(request, 'email.html', context)

def invoice(request):
    amount = 0
    tempamount = 0
    total = 0
    quantity =[]
    cart = request.session.get('cart')
    wi = Website_Info.objects.all()
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    for items in products:
        tempamount = (items.Product_Price * cart.get(str(items.Product_ID)))
        amount += tempamount
        quantity.insert(len(quantity),cart.get(str(items.Product_ID)))
    total = amount
    # for items in quantity:
    #     print(items)
    # res = quantity
    # list(map(lambda x:x, res))
    # print(res)
    if request.method == 'GET':
        user = request.session.get('user')
        # print(user)
        orders = Order_Request.objects.filter(Customer= user).order_by('-Date')
        total = amount
        
        # orders = orders.reverse()
        # print(orders)
        context = {
            'total': total,
            'orders': orders,
            'pr': products,
            'wi':wi,
            'qty': quantity,
            'time': x
        }
    return render(request, 'invoice.html',context)

def change_password(request, pk):
    wi = Website_Info.objects.all()
    userid = User_Details.objects.get(User_ID = pk)
    ids = list(request.session.get('cart').keys())  
    products = Product_Details.objects.filter(Product_ID__in = ids)
    if request.method == 'GET':
        return render(request, 'change_password.html',{'userid' : userid})
    if request.method == 'POST':
        postData = request.POST
        currentpass = postData.get('currentpass')
        pass1 = postData.get('pass1')
        pass2 = postData.get('pass2')
        userid.Password = postData.get('pass1')

        value = {
            'userid' : userid,
            'currentpass' : currentpass,
            'pass1' : pass1,
            'pass2' : pass1,
            'wi': wi,
        }


        error_message = None
        uspass = User_Details.objects.get(User_ID = pk )
        # print(uspass)
        print(uspass)
        
        if not uspass.Password == currentpass:
            error_message = 'Old Password Does not match'
        else:
            # print(uspass.Password)
            if pass1 != pass2:
                error_message = 'New password does not match'
        if len(pass1) < 6:
            error_message = 'Password must be 6 characters long'
        if not error_message:
            userid.save()
            return redirect('userprofile', pk)
        else:
            data = {
                'error': error_message,
                'values': value,
                }    
        return render(request, 'change_password.html', data)

def contact_us(request):
    wi = Website_Info.objects.all()
    context = {
        'wi': wi,
    }
    return render(request, 'thankyou.html', context)
