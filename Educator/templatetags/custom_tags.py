
from django import template 
from Educator.models import *
import math
register = template.Library() 



@register.simple_tag
def Price_After_discount(price,discount):
    if discount is None or discount is 0:
        return price
    else:
        sellprice=price
        sellprice=price-(price* discount * 0.01)
        return math.floor(sellprice)    


@register.filter
def rupee(price):
    return f'Rs. {price}' 

@register.simple_tag
def is_enrolled(request,course):
    user=None
    if request.user.is_authenticated is False:
        return False
    user =request.user
    
    try:
        user_course = UserCourse.objects.get(user=user,course=course)
        return True
    except:
        return False

