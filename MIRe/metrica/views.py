from django.shortcuts import render
from .models import Metrica
from django.http import HttpResponse,  JsonResponse
from .forms import MetricaForm 


# Create your views here.

def index(request):
    
    print('hola mundo')
    return render(request, 'index.html')



#def create(request):
  #  form = MetricaForm()

   # return render(request, 'create.html', {'form' : form}) 

