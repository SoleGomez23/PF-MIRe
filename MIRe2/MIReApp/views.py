from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Indicador, Metrica, HistorialMetrica
from .forms import MetricaForm
from .forms import MetricaFormEditar
from .forms import IndicadorFormEditar
from .forms import IndicadorForm
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import JsonResponse

def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def error(request):
    return render(request, 'paginas/error.html')

def metricas(request):#el renderizado se hace acá, por eso tenemos el libro incrustado en el index, eso se soluciona acá
    metricas = Metrica.objects.all()
    return render(request, 'metricas/index.html', {'metrica': metricas})

def indicadores(request):#el renderizado se hace acá, por eso tenemos el libro incrustado en el index, eso se soluciona acá
    indicadores = Indicador.objects.all()
    return render(request, 'indicadores/indexindicador.html', {'indicador': indicadores})

def crear_metricas(request):
    formulario = MetricaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, '¡Métrica creada exitosamente!')
        return redirect('metricas')
    return render(request, 'metricas/crear.html', {'formulario': formulario})  

def crear_indicadores(request):
    formulario2 = IndicadorForm(request.POST or None, request.FILES or None)
    if formulario2.is_valid():
        formulario2.save()
        messages.success(request, '¡Indicador creado exitosamente!')
        return redirect('indicadores')
    return render(request, 'indicadores/crear.html', {'formulario2': formulario2})  

def editar_metricas(request, id):
    metrica = get_object_or_404(Metrica, id=id)
    formulario = MetricaFormEditar(request.POST or None, request.FILES or None, instance=metrica)
    if request.method == 'POST':
        formulario = MetricaFormEditar(request.POST, instance=metrica)
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

def editar_indicadores(request, id):
    indicador = get_object_or_404(Indicador, id=id)
    formulario2 = IndicadorFormEditar(request.POST or None, request.FILES or None, instance=indicador)
    if request.method == 'POST':
        formulario2 = IndicadorFormEditar(request.POST, instance=indicador)
        if formulario2.is_valid():
            formulario2.save()
        return redirect('indicadores')
    else:
        form = IndicadorForm(instance = indicador)
    return render(request, 'indicadores/editar.html', {'formulario2': formulario2})

def eliminar_indicadores(request, id):
    indicadores = Indicador.objects.get(id=id)
    indicadores.delete()
    return redirect('indicadores')



def historial_metrica(request, metrica_id):
    metrica = Metrica.objects.get(id=metrica_id)
    historial = HistorialMetrica.objects.filter(metrica=metrica).order_by('-año_historico')

    if request.method == 'POST':
        nuevo_año = int(request.POST['nuevo_año'])
        nuevo_valor = int(request.POST['nuevo_valor'])

        # Verificar si el nuevo año ya está en el historial
        if HistorialMetrica.objects.filter(metrica=metrica, año_historico=nuevo_año).exists():
            messages.error(request, 'Error: La instancia ingresada ya está registrada en el historial.')
        else:
            historial_metrica = HistorialMetrica(metrica=metrica, año_historico=nuevo_año, valor_historico=nuevo_valor)
            historial_metrica.save()
            messages.success(request, '¡Instancia creada exitosamente!')

            metrica.valor = nuevo_valor
            metrica.save()

        return redirect('historial_metrica', metrica_id=metrica_id)

    return render(request, 'historial_metrica.html', {'metrica': metrica, 'historial': historial})

def eliminar_historial_metrica(request, historial_id):
    historial = HistorialMetrica.objects.get(id=historial_id)
    historial.delete()
    return JsonResponse({"success": True})