from django.shortcuts import render
from errands.models import Category

def home(request):
    categories = Category.objects.all()[:6]  # Get first 6 categories
    return render(request, 'home.html', {'categories': categories}) 


