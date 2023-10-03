from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Indicador, Metrica, HistorialMetrica, Tipo
from .forms import MetricaForm
from .forms import MetricaFormEditar
from .forms import IndicadorFormEditar
from .forms import IndicadorForm
from .forms import IndicadorFormVer
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import JsonResponse
import json

def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def error(request):
    return render(request, 'paginas/error.html')

def metricas(request):
    metricas = Metrica.objects.all()
    ultimos_valores = list()
    for u in metricas:
        if HistorialMetrica.objects.filter(metrica=u.id).order_by('año_historico'):
            t = list(HistorialMetrica.objects.filter(metrica=u.id).order_by('año_historico'))[-1]
            u.valor = str(t.valor_historico)
            u.year = str(t.año_historico)
    return render(request, 'metricas/index.html', {'metrica': metricas})

def indicadores(request):
    indicadores = Indicador.objects.all()
    return render(request, 'indicadores/indexindicador.html', {'indicador': indicadores})

def crear_metricas(request):
    formulario = MetricaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        band = True
        formulario.save()
        messages.success(request, '¡Métrica creada exitosamente!', extra_tags='alta-exitosa')
        t = Metrica.objects.get(titulo=formulario.cleaned_data['titulo'])
        if t.frecuencia == 'Anual':
            historial_metrica(request, t.id, t.valor, t.year, band)
        elif t.frecuencia == 'Mensual':
            historial_metrica(request, t.id, t.valor, t.year, t.month, band)
        return redirect('metricas')
    return render(request, 'metricas/crear.html', {'formulario': formulario})  

def crear_indicadores(request):
    if request.method == 'POST':
        formulario2 = IndicadorForm(request.POST or None, request.FILES or None)   
        if formulario2.is_valid():
            formulario2.save()
            messages.success(request, '¡Indicador creado exitosamente!', extra_tags='alta-exitosa')
            return redirect('indicadores')
        else:
            print_fields(request)
        # Obtener la lista de métricas para mostrar en la tabla
    else:
        formulario2 = IndicadorForm()

    metricas = Metrica.objects.all()        
    context = { 'formulario2': formulario2, 'metricas': metricas }

    return render(request, 'indicadores/crear.html', context)

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
    messages.success(request, '¡Metrica eliminada exitosamente!', extra_tags='alta-exitosa')
    return redirect('metricas')

def editar_indicadores(request, id):
    indicador = get_object_or_404(Indicador, id=id)
    formulario2 = IndicadorFormEditar(request.POST or None, request.FILES or None, instance=indicador)
    if request.method == 'POST':
        formulario2 = IndicadorFormEditar(request.POST, instance=indicador)
        if formulario2.is_valid():
            formulario2.save()
        messages.success(request, '¡Cambios guardados exitosamente!', extra_tags='alta-exitosa')    
        return redirect('indicadores')
    
    return render(request, 'indicadores/editar.html', {'formulario2': formulario2, 'indicador':indicador})

def ver_indicador(request, id):
    indicador = get_object_or_404(Indicador, id=id)
    return render(request, 'indicadores/indicador.html', {'indicador': indicador})

def eliminar_indicadores(request, id):
    indicadores = Indicador.objects.get(id=id)
    indicadores.delete()
    messages.success(request, '¡Indicador eliminado exitosamente!', extra_tags='alta-exitosa')
    return redirect('indicadores')

def historial_metrica(request, metrica_id, valor=0, año=0, mes=0, band=False):
    metrica = Metrica.objects.get(id=metrica_id)
    historial = HistorialMetrica.objects.filter(metrica=metrica).order_by('-año_historico')

    if band:
        if metrica.frecuencia == 'Anual':
            print(año)
            historial_metrica = HistorialMetrica(metrica=metrica, año_historico=año, valor_historico=valor)
            historial_metrica.save()
        elif metrica.frecuencia == 'Mensual':
            print(año)
            historial_metrica = HistorialMetrica(metrica=metrica, año_historico=año, mes_historico=mes, valor_historico=valor)
            historial_metrica.save()
        
    else:

        if request.method == 'POST':
            nuevo_año = int(request.POST['nuevo_año'])
            nuevo_mes = request.POST['nuevo_mes']
            nuevo_valor = int(request.POST['nuevo_valor'])

            # Verificar si el nuevo año ya está en el historial
            if metrica.frecuencia == 'Anual':
                if HistorialMetrica.objects.filter(metrica=metrica, año_historico=nuevo_año).exists():
                    messages.error(request, 'Error: La instancia ingresada ya está registrada en el historial.')
                else:
                    historial_metrica = HistorialMetrica(metrica=metrica, año_historico=nuevo_año, valor_historico=nuevo_valor)
                    historial_metrica.save()
                    messages.success(request, '¡Instancia creada exitosamente!', extra_tags='alta-exitosa')
            elif metrica.frecuencia == 'Mensual':
                if HistorialMetrica.objects.filter(metrica=metrica, año_historico=nuevo_año, mes_historico=nuevo_mes).exists():
                    messages.error(request, 'Error: La instancia ingresada ya está registrada en el historial.')
                else:
                    historial_metrica = HistorialMetrica(metrica=metrica, año_historico=nuevo_año, mes_historico=nuevo_mes, valor_historico=nuevo_valor)
                    historial_metrica.save()
                    messages.success(request, '¡Instancia creada exitosamente!', extra_tags='alta-exitosa')

            return redirect('historial_metrica', metrica_id=metrica_id)

        return render(request, 'historial_metrica.html', {'metrica': metrica, 'historial': historial})


def eliminar_historial_metrica(request, historial_id):
    historial = HistorialMetrica.objects.get(id=historial_id)
    historial.delete()
    return JsonResponse({"success": True})

def tipos(request):
    data = json.loads(request.body)
    tipos = Tipo.objects.filter(ambito__id=data['user_id'])
    print(tipos)
    return JsonResponse(list(tipos.values("id", "nombre")), safe=False)

def instancias(request):
    data = json.loads(request.body)
    print(data['user_id'])
    instances = HistorialMetrica.objects.filter(metrica__id=data['user_id'])
    print(instances)
    return JsonResponse(list(instances.values("id", "año_historico")), safe=False)

def medidas(request):
    data = json.loads(request.body)
    metrics = Metrica.objects.filter(id=data['user_id'])
    print('ggggggggggggg')
    print(metrics)
    return JsonResponse(list(metrics.values("unidad_medida")), safe=False)

def valores(request):
    data = json.loads(request.body)
    print(data['user_id'])
    instances = HistorialMetrica.objects.filter(id=data['user_id'])
    print(instances)
    return JsonResponse(list(instances.values("id", "valor_historico")), safe=False)

def print_fields(request):#esta vista solo sirve para debugear
    print('nombre: '+ request.POST["nombre"])
    print('descripcion: ' + request.POST["descripcion"])
    print('frecuencia: ' + request.POST["frecuencia"])
    print('ambito: ' + request.POST["ambito"])
    print('tipo: ' + request.POST["tipo"])
    print('formula: ' + request.POST["formula"])
    print('numerador: ' + request.POST["numerador"])
    print('denominador: ' + request.POST["denominador"])
    print('numerador_periodo: ' + request.POST["numerador_periodo"])
    print('denominador_periodo: ' + request.POST["denominador_periodo"])
    print('numerador_medida: ' + request.POST["numerador_medida"])
    print('denominador_medida: ' + request.POST["denominador_medida"])
    print('numerador_valor: ' + request.POST["numerador_valor"])
    print('denominador_valor: ' + request.POST["denominador_valor"])
    print('resultado: ' + request.POST["resultado"])


