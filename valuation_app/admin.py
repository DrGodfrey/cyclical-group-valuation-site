from django.contrib import admin

from .models import Company_model, CircularOwnership_model

# Register your models here.

admin.site.register(Company_model)
# admin.site.register(CircularOwnership_model) - not working, due to many-to-many-relationship?