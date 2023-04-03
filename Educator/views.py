# Create your views here.
from OnlineCourse.settings import KEY_ID, KEY_SECRET
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User,auth
import razorpay
from time import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

def index(request):
    course= Course.objects.all()
    trainer=Trainer.objects.all()          
    #for Contactform data
    if request.method == 'POST':
        contact=Contact()
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        message = request.POST['message']
        contact.first_name=first_name
        contact.last_name=last_name
        contact.email=email
        contact.mobile_number=mobile
        contact.message=message
        contact.save()
    return render(request,'index.html',{'course':course,'trainer':trainer})

# for Registration
def registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists")
                return redirect('registration')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email already exists")
                return redirect('registration')
            else:
                user = User.objects.create_user(username=username,email=email,first_name=name,password=password) 
                user.save();
                return redirect('login')
                
        else:
            messages.info(request,"password not matching.....")
            return redirect('registration')   
    else:
        return render(request,'registration.html')    

# for Login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        next_page=request.GET.get('next')
        if user is not None:
            auth.login(request,user)
            if next_page is not None:
                return redirect(next_page)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials') 
            return redirect('login')   

    else:    
        return render(request,'login.html')        

# for Logout
def logout(request):
    auth.logout(request)
    return redirect('/')        

# for Courses
def courses(request):
    course= Course.objects.all()
    return render(request,'courses.html',{'course':course}) 

# for Course-details
def courseDetails(request,slug):
    course= Course.objects.get(slug = slug)
    serial_number=request.GET.get('lecture')
    videos = course.video_set.all().order_by('serial_number')
    if serial_number is None:
        serial_number= 1
    video = Video.objects.get(serial_number=serial_number,course=course)

    if video.is_preview is False:
        if request.user.is_authenticated is False:
            return redirect('login')
        else:
            user=request.user
            try:
                user_course = UserCourse.objects.get(user=user,course=course)
            except:
                return redirect('checkOut',slug=course.slug)
            
    return render(request,'course-details.html',{'course':course,'video':video,'videos':videos}) 

# for checkout
@login_required(login_url="login")
def checkOut(request,slug):
    course= Course.objects.get(slug = slug)
    user=None
    if request.user.is_authenticated is False:
        return redirect('login')
    user =request.user
    action=request.GET.get('action')
    order = None
    payment=None
    error=None
    coupon_code_message=None
    coupon=None
    amount  = (course.price-(course.price * course.discount * 0.01)) * 100
    amount = int(amount)
    couponcode=request.GET.get('couponcode')
    
    try:
        user_course = UserCourse.objects.get(user=user,course=course)
        error = "You Are already Enrolled in this course .."
        return redirect('my_courses')
    except:
        pass

    if error is None:
            amount  = (course.price-(course.price * course.discount * 0.01)) * 100
            amount = int(amount) 
    if couponcode:
        try:
            coupon= CouponCode.objects.get(course=course, couponcode=couponcode)
            amount = (course.price - (course.price * coupon.discount * 0.01)) * 100
            amount=int(amount)
        except:
            coupon_code_message = "Invalid Coupon Code" 


    if amount==0:
        user_course = UserCourse(user=user,course=course)
        try:
            user_course = UserCourse.objects.get(user=user,course=course)
            error = "You Are already Enrolled in this course .."
        except:
            pass

        user_course.save()
        return redirect('my_courses')


    if action == 'create_payment':
 
        currency = "INR"
        receipt = f"Educator-{int(time())}"
        notes={
            'email': user.email,
            'name':user.username
        }
        order= client.order.create({'amount':amount,'currency':currency,'receipt':receipt,'notes':notes})
        payment = Payment()
        payment.user = user
        payment.course = course
        payment.order_id= order.get('id')
        payment.save()

    context={
            "course":course,
            "order":order,
            "payment":payment,
            "user":user,
            "error":error,
            "amount":amount,
            "coupon_code_message":coupon_code_message,
            "coupon":coupon    
        }
    return render(request,template_name='check-out.html',context=context)     



@login_required(login_url="login")
def my_courses(request):
    user=request.user
    user_course = UserCourse.objects.filter(user=user)        
    return render(request,'my_courses.html',{'user_course':user_course}) 
        

@csrf_exempt
def verify_payment(request):
    if request.method =="POST":
        data=request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id=data['razorpay_order_id']
            razorpay_payment_id=data['razorpay_payment_id']

            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status=True
            user_course = UserCourse(user=payment.user,course=payment.course)
            user_course.save()

            payment.user_course=user_course
            payment.save()

            return redirect('my_courses')
        except:
            return HttpResponse('Invalid Payment Details')    
    


