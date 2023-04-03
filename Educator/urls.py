from django.urls import path
from . import views

urlpatterns = [
   path('',views.index, name="index"),
   path('login/',views.login, name="login"),
   path('logout/',views.logout, name="logout"),
   path('registration/',views.registration, name="registration"),
   path('courses/',views.courses, name="courses"),
   path('check-out/<str:slug>',views.checkOut, name="checkOut"),
   path('course-details/<str:slug>',views.courseDetails, name="courseDetails"),
   path('verify_payment/',views.verify_payment, name="verify_payment"),
   path('my_courses/',views.my_courses, name="my_courses"),
]