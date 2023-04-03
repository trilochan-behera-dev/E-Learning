from django.contrib.auth.models import User
from django.db import models


# For Trainer Model
class Trainer(models.Model):
    trainer_name= models.CharField(max_length=100)
    trainer_course= models.CharField(max_length=100)
    trainer_image= models.ImageField(upload_to='Trainer_images')
    def __str__(self):
        return self.trainer_name


# For Contact Model
class Contact(models.Model):
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    mobile_number= models.CharField(max_length=100)
    email= models.EmailField()
    message=models.TextField()
    def __str__(self):
        return self.first_name + ' ' + self.last_name


# For Course Model
class Course(models.Model):
    course_name= models.CharField(max_length=100, null=False)
    slug= models.CharField(max_length=100, null=False, unique=True)
    course_image= models.ImageField(upload_to='Course_images')
    course_length=models.IntegerField(null=False)
    description= models.TextField(null=False)
    price= models.IntegerField(null=False)
    discount=models.IntegerField(null=False,default=0)
    resource=models.FileField(upload_to='resource')
    date=models.DateTimeField(auto_now_add=True)    
    active=models.BooleanField(default=False)
    
    def __str__(self):
        return self.course_name

# For CourseProperty
class CourseProperty(models.Model):
    description=models.CharField(max_length=100,null=False)
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Tag(CourseProperty) :
    pass 
class Prerequisite(CourseProperty) :
    pass  
class Learning(CourseProperty) :
    pass 


# For Video Section
class Video(models.Model):
    title= models.CharField(max_length=100,null=False)
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    serial_number= models.IntegerField(null=False)
    video_id=models.CharField(max_length=100,null=False)
    is_preview=models.BooleanField(default=False)
    def __str__(self):
        return self.course.course_name + " " + str(self.serial_number)


# For Video Section
class UserCourse(models.Model):
    user=models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + " - " + str(self.course.course_name)

# For Video Section
class Payment(models.Model):
    order_id= models.CharField(max_length=100,null=False)
    payment_id= models.CharField(max_length=100,null=True)
    user_course= models.ForeignKey(UserCourse,null=True,blank = True, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)
    def __str__(self):
       return self.user.username + " - " + str(self.course.course_name) + " - " +str(self.order_id)


class CouponCode(models.Model):
    couponcode=models.CharField(max_length=20)
    course=models.ForeignKey(Course, on_delete=models.CASCADE,related_name='coupons')
    discount = models.IntegerField(default = 0)
    def __str__(self):
       return self.course.course_name + " - " +str(self.couponcode)



