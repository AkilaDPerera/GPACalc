from django.contrib import admin

from gpa.models import Module
from gpa.models import Semester
from gpa.models import Feedback
from gpa.models import Performance
from gpa.models import Profile
from gpa.models import MarkSheet

# Register your models here.
admin.site.register(Module)
admin.site.register(Semester)
admin.site.register(Feedback)
admin.site.register(Performance)
admin.site.register(Profile)
admin.site.register(MarkSheet)
