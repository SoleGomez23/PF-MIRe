from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Metrica, HistorialMetrica
from .forms import MetricaForm
from .forms import MetricaFormEditar
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
    ultimos_valores = list()
    for u in metricas:
        if HistorialMetrica.objects.filter(metrica=u.id).order_by('año_historico'):
            t = list(HistorialMetrica.objects.filter(metrica=u.id).order_by('año_historico'))[-1]
            u.valor = str(t.valor_historico)+' ('+str(t.año_historico)+')'
    return render(request, 'metricas/index.html', {'metrica': metricas})

def crear_metricas(request):
    formulario = MetricaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        band = True
        formulario.save()
        messages.success(request, '¡Métrica creada exitosamente!')
        t = Metrica.objects.get(titulo=formulario.cleaned_data['titulo'])
        if t.year:
            historial_metrica(request, t.id, t.valor, t.year, band)
        return redirect('metricas')
    return render(request, 'metricas/crear.html', {'formulario': formulario})  

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

def historial_metrica(request, metrica_id, valor=0, año=0, band=False):
    metrica = Metrica.objects.get(id=metrica_id)
    historial = HistorialMetrica.objects.filter(metrica=metrica).order_by('-año_historico')

    if band:
        print(año)
        historial_metrica = HistorialMetrica(metrica=metrica, año_historico=año, valor_historico=valor)
        historial_metrica.save()
        
    else:

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

            return redirect('historial_metrica', metrica_id=metrica_id)

        return render(request, 'historial_metrica.html', {'metrica': metrica, 'historial': historial})

def eliminar_historial_metrica(request, historial_id):
    historial = HistorialMetrica.objects.get(id=historial_id)
    historial.delete()
    return JsonResponse({"success": True})