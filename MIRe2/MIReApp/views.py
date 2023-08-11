from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Metrica
from .forms import MetricaForm
from django.shortcuts import get_object_or_404, render

def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def error(request):
    return render(request, 'paginas/error.html')

def metricas(request):#el renderizado se hace acá, por eso tenemos el libro incrustado en el index, eso se soluciona acá
    metricas = Metrica.objects.all()
    return render(request, 'metricas/index.html', {'metrica': metricas})

def crear_metricas(request):
    formulario = MetricaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('metricas')
    return render(request, 'metricas/crear.html', {'formulario': formulario})  

def editar_metricas(request, id):
    metrica = get_object_or_404(Metrica, id=id)
    formulario = MetricaForm(request.POST or None, request.FILES or None, instance=metrica)
    if request.method == 'POST':
        formulario = MetricaForm(request.POST, instance=metrica)
        if formulario.is_valid():
            formulario.save()
        return redirect('metricas')
    else:
        form = MetricaForm(instance = metrica)
    return render(request, 'metricas/editar.html', {'formulario': formulario})

def eliminar_metricas(request, id):
    metricas = Metrica.objects.get(id=id)
    metricas.delete()
    return redirect('metricas')