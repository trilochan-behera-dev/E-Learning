from django.contrib import admin
from .models import *

# Register your models here.
class TagAdmin(admin.TabularInline):
    model =Tag
class LearningAdmin(admin.TabularInline):
    model =Learning
class PrerequisiteAdmin(admin.TabularInline):
    model =Prerequisite
class VideoAdmin(admin.TabularInline):
    model = Video

class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin,LearningAdmin,PrerequisiteAdmin,VideoAdmin]

admin.site.register(Contact)
admin.site.register(Trainer)
admin.site.register(Video)
admin.site.register(Payment)
admin.site.register(CouponCode)
admin.site.register(UserCourse)
admin.site.register(Course,CourseAdmin)