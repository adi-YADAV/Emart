from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import Product,Cart,Order
from django.db.models import Q
import razorpay
from django.core.mail import send_mail

# Create your views here.
def product(request):
    #p=Product.objects.all()
    p=Product.objects.filter(is_active=True)
    #print(p)
    #context={'data':p}
    context={}
    context['data']=p

    return render(request,'index.html',context)

def register(request):
    context={}
    if request.method =='GET':
        return render(request,'register.html')
    else:
        un=request.POST['uname']
        ue=request.POST['uemail']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        """print(un)
        print(ue)
        print(p)
        print(cp)"""
        if un==''or ue=='' or p == '' or cp =='':
            #print("al fields required")
            context['ermsg']="all fields required"
            return render(request,'register.html',context)
        elif p!=cp:
            #print("Password does not match")
            context['ermsg']="Password does not match"
            return render(request,'register.html',context)
        elif len(p)<8:
            #print("password must be of minimum 8 characters")
            context['ermsg']="password must be of minimum 8 characters"
            return render(request,'register.html',context)
        else:
            u=User.objects.create(username=un,email=ue)
            u.set_password(p)
            u.save()
            context['success']="Data saved successfully...!"
            return render(request,'register.html',context)
        
def ulogin(request):
    context={}
    if request.method=='GET':
        return render(request,'login.html')
    else:
        n= request.POST['uname']
        p= request.POST['upass']
        #print(n," ",p)
        e= authenticate(username=n,password=p)
        print(e)
        if e is not None:
            login(request,e)
            return redirect('/product')
        else:
            context['ermsg']='Invalid Username or Password'
            return render(request,'login.html',context)


def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def user_logout(request):
    logout(request)
    return redirect('/product') 

def catfilter(request,cv):
    #print(cv)
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def sortfilter(request,sv):
    if sv=='1':
        p=Product.objects.order_by('-price').filter(is_active=True)
    else:
        p=Product.objects.order_by('price')
    
    context={}
    context['data']=p
    return render(request,'index.html',context)

def pricefilter(request):
    min=request.GET['min']
    max=request.GET['max']
    #print(min)
    #print(max)
    q1=Q(price__gte =min)
    q2=Q(price__lte =max)
    p=Product.objects.filter(q1&q2).filter(is_active=True )
    context={}
    context['data']=p
    return render(request,'index.html',context)

def search(request):
    s=request.GET['search']
    #print(s)
    pname=Product.objects.filter(name__icontains=s)
    pcat=Product.objects.filter(cat__icontains=s)
    pdet=Product.objects.filter(pdetail__icontains=s)
    allprod=pname.union(pcat,pdet)
    context={}

    if allprod.count()==0:
        context['errmsg']='Product not Found...!'
  
    context['data']=allprod
    return render(request,'index.html',context)

def product_detail(request,pid):
    #print(pid)
    context={}
    p=Product.objects.filter(id=pid)
    context['data']=p
    return render(request,'product_detail.html',context)

def addtocart(request,pid):
    #print(pid) 
    if request.user.is_authenticated:
        #print('user is logged in')
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        context={}
        context['data']=p
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        if n==0:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']='Product added successfully to cart....!'
        else:
            context['ermsg']='Product already exists in cart...!'
        return render(request,'product_detail.html',context)

    else:
        return redirect('/ulogin')
    
def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    #print(c)
    context={}
    s=0
    for i in c:
        s=s+i.pid.price*i.qty

    context['total']=s
    context['n']=len(c)
    context['data']=c
    return render(request,'cart.html',context)


def updateqty(request,u,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if u=='1':
        q+=1
    elif q>1:
        q-=1
    c.update(qty=q)
    return redirect('/viewcart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect(request,'/viewcart')

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    hn=request.POST['hno']
    lane=request.POST['lane']
    area=request.POST['area']
    city=request.POST['city']
    pin=request.POST['pin']
    #print(c)
    for i in c:
        amount=i.qty*i.pid.price
        
        o=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=amount,house_no=hn,lane=lane,area=area,city=city,pin=pin)
        o.save()
        i.delete()
       
    #return render(request,'placeorder.html')
    return redirect('/fetchorder')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    context={} 
    q=0
    tamount=0
    for i in o:
        q=q+i.qty
        tamount=tamount+(i.qty*i.pid.price)
    context['total']=tamount
    context['n']=q
    context['data']=o
    return render(request,'placeorder.html',context)

    


def history(request,uid):
    h=Order.objects.filter(uid=uid)
    context={}
    context['data']=h
    return render(request,'history.html',context)

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_CbepQPSX6Lp3CN", "dk1YgCyVZRSVoUT1OGNgjWC0"))
    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt 
    data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    #print(payment)
    context={}
    context['payment']=payment
    return render(request,'pay.html',context)

def paymentsuccess(request):
    return render(request,'paymentsuccess.html')



def paymentsuccess(request):
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    sub='E-Commerce Order Status'
    msg='Thanks For Shopping'
    frm ='adiyadav2019@gmail.com'
    send_mail(
        sub, 
        msg, 
        frm, 
        [to], 
        fail_silently=False
    )
    
    return render(request,'paymentsuccess.html')