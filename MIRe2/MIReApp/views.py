from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Indicador, Metrica, HistorialMetrica, Tipo, Programa, Ambito, Objetivos
from .forms import MetricaForm, MetricaFormEditar, IndicadorForm, IndicadorFormEditar, InstanciaForm, ProgramaForm,ProgramaFormEditar, ObjetivoForm
import json
from django.db.utils import IntegrityError  # Importa la excepción de integridad

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
            t = list(HistorialMetrica.objects.filter(metrica=u.id).order_by('año_historico'))[-1] #Obtengo el la ultima instancia de la metrica
            u.valor = str(t.valor_historico) #Agrego en el campo valor, el valor de la ultima instancia 
            u.year = str(t.año_historico) #Agrego en el campo año, el año de la ultima instancia
    return render(request, 'metricas/index.html', {'metrica': metricas})

def indicadores(request):
    indicadores = Indicador.objects.all()
    tipos = Tipo.objects.all()
    ambitos = Ambito.objects.all()
    programas = Programa.objects.all()
    return render(request, 'indicadores/index.html', {'indicador': indicadores,'tipos': tipos,'ambitos': ambitos,'programas': programas,})

def crear_metricas(request):
    formulario = MetricaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        band = True 
        formulario.save()
        messages.success(request, '¡Métrica creada exitosamente!', extra_tags='alta-exitosa')
        t = Metrica.objects.get(titulo=formulario.cleaned_data['titulo']) 
        historial_metrica(request, t.id, t.valor, t.year2, t.year, t.semestral, t.month, band) #Le paso los valores de la metrica a historial_metrica para crear su primera instancia
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
        formulario2 = IndicadorForm()

    metricas = Metrica.objects.all()     
    programas = Programa.objects.all()   
    objetivos = Objetivos.objects.all()      
    context = { 'formulario2': formulario2, 'metricas': metricas, 'programas':programas, 'objetivos': objetivos}

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

def eliminar_indicador(request, id):
    indicadores = Indicador.objects.get(id=id)
    indicadores.delete()
    messages.success(request, '¡Indicador eliminado exitosamente!', extra_tags='alta-exitosa')
    return redirect('indicadores')

def historial_metrica(request, metrica_id, valor=0, año2=0, año=0, semestral=0, mes=0, band=False):
    metrica = Metrica.objects.get(id=metrica_id)
    formulario = InstanciaForm(request.POST or None, request.FILES or None)
    historial = HistorialMetrica.objects.filter(metrica=metrica).order_by('-año_historico')
    
    if band: #Si band es true entro a historial_metrica porque una metrica acaba de ser creada, entonces se debe crear su primera instancia con los datos que recibio por parametro
        historial_metrica = HistorialMetrica(metrica=metrica, año2_historico=año2, año_historico=año, semestre_historico=semestral, mes_historico=mes, valor_historico=valor)
        historial_metrica.save()
        
    else: #Si band es falso, no es una metrica nueva

        if request.method == 'POST':
            nuevo_año = int(request.POST['año_historico']) #Obteniene el año que quiere ingresar el usuario
            nuevo_valor = int(request.POST['valor_historico']) #Obteniene el valor que quiere ingresar el usuario

            # Verificar si el nuevo año ya está en el historial
            if metrica.frecuencia == 'Anual':
                if HistorialMetrica.objects.filter(metrica=metrica, año_historico=nuevo_año).exists():
                    messages.error(request, 'Error: La instancia ingresada ya está registrada en el historial.')
                else:
                    historial_metrica = HistorialMetrica(metrica=metrica, año_historico=nuevo_año, valor_historico=nuevo_valor)
                    historial_metrica.save()
                    messages.success(request, '¡Instancia creada exitosamente!', extra_tags='alta-exitosa')
            elif metrica.frecuencia == 'Mensual':
                nuevo_mes = request.POST['mes_historico']
                if HistorialMetrica.objects.filter(metrica=metrica, año_historico=nuevo_año, mes_historico=nuevo_mes).exists():
                    messages.error(request, 'Error: La instancia ingresada ya está registrada en el historial.')
                else:
                    historial_metrica = HistorialMetrica(metrica=metrica, año_historico=nuevo_año, mes_historico=nuevo_mes, valor_historico=nuevo_valor)
                    historial_metrica.save()
                    messages.success(request, '¡Instancia creada exitosamente!', extra_tags='alta-exitosa')
            elif metrica.frecuencia == 'Semestral':                
                nuevo_semestre = request.POST['semestre_historico']
                if HistorialMetrica.objects.filter(metrica=metrica, año_historico=nuevo_año, semestre_historico=nuevo_semestre).exists():
                    messages.error(request, 'Error: La instancia ingresada ya está registrada en el historial.')
                else:
                    historial_metrica = HistorialMetrica(metrica=metrica, año_historico=nuevo_año, semestre_historico=nuevo_semestre, valor_historico=nuevo_valor)
                    historial_metrica.save()
                    messages.success(request, '¡Instancia creada exitosamente!', extra_tags='alta-exitosa')
            elif (metrica.frecuencia == 'Bianual') or (metrica.frecuencia == 'Cuatrianual' ):
                nuevo_año2 = int(request.POST['año2_historico'])
                if HistorialMetrica.objects.filter(metrica=metrica, año_historico=nuevo_año, año2_historico=nuevo_año2).exists():
                    messages.error(request, 'Error: La instancia ingresada ya está registrada en el historial.')
                else:
                    historial_metrica = HistorialMetrica(metrica=metrica, año_historico=nuevo_año, año2_historico=nuevo_año2, valor_historico=nuevo_valor)
                    historial_metrica.save()
                    messages.success(request, '¡Instancia creada exitosamente!', extra_tags='alta-exitosa')

            return redirect('historial_metrica', metrica_id=metrica_id)

        return render(request, 'instancias/index.html', {'metrica': metrica, 'historial': historial, 'formulario':formulario})

def eliminar_historial_metrica(request, historial_id):
    historial = HistorialMetrica.objects.get(id=historial_id)
    historial.delete()
    return JsonResponse({"success": True})

def tipos(request):
    data = json.loads(request.body)
    tipos = Tipo.objects.filter(ambito__id=data['user_id'])
    return JsonResponse(list(tipos.values("id", "nombre")), safe=False)

def ambitos(request):
    data = json.loads(request.body)
    ambitos = Ambito.objects.filter(ambito__id=data['user_id'])
    return JsonResponse(list(ambitos.values("id", "nombre")), safe=False)

def instancias(request):
    data = json.loads(request.body)
    metrics = Metrica.objects.filter(id=data['user_id'])
    frec2 = list(metrics.values("frecuencia"))
    frec = frec2[0]["frecuencia"]
    instances = HistorialMetrica.objects.filter(metrica__id=data['user_id'])
    data = [{'id': instance['id'], 'año_historico': instance['año_historico'], 'año2_historico': instance['año2_historico'], 'semestre_historico': instance['semestre_historico'], 'mes_historico': instance['mes_historico'], 'frecuencia': frec} for instance in instances.values() ]
    return JsonResponse(data, safe=False)

def medidas(request):
    data = json.loads(request.body)
    metrics = Metrica.objects.filter(id=data['user_id'])
    return JsonResponse(list(metrics.values("unidad_medida")), safe=False)

def valores(request):
    data = json.loads(request.body)
    instances = HistorialMetrica.objects.filter(id=data['user_id'])
    return JsonResponse(list(instances.values("id", "valor_historico")), safe=False)

def listarMetricas(request):
    data = json.loads(request.body)
    metricas = Metrica.objects.filter(frecuencia=data['user_id'])
    print(list(metricas.values("id", "titulo")))
    return JsonResponse(list(metricas.values("id", "titulo")), safe=False)

def programas(request):
    programs = Programa.objects.all()
    return render(request, 'programas/index.html', {'programas': programs})

def crear_programa(request):

    if request.method == 'POST':
        formulario = ProgramaForm(request.POST or None, request.FILES or None)   
        if formulario.is_valid():
            formulario.save()
            prog = Programa.objects.get(nombre=formulario.cleaned_data['nombre'])
            crear_objetivo(prog.id, prog.objetivo)
            messages.success(request, '¡Programa creado exitosamente!', extra_tags='alta-exitosa')
            return redirect('programas')
    else:
        formulario = ProgramaForm()
        
    context = { 'formulario': formulario }

    return render(request, 'programas/crear.html', context)

def editar_programas(request, id):
    programa = get_object_or_404(Programa, id=id)
    formulario = ProgramaFormEditar(request.POST or None, request.FILES or None, instance=programa)
    if request.method == 'POST':
        try:
            if formulario.is_valid():
                formulario.save()
                messages.success(request, '¡Cambios guardados exitosamente!', extra_tags='modificación-exitosa')
                return redirect('programas')
            else:
                print(formulario.errors)
        except IntegrityError as e:
            messages.error(request, 'Error al guardar los cambios: {}'.format(e), extra_tags='error-guardado')
    
    return render(request, 'programas/editar.html', {'formulario': formulario, 'programa':programa})

def eliminar_programas(request, id):
    programas = Programa.objects.get(id=id)
    programas.delete()
    messages.success(request, 'Programa eliminado exitosamente', extra_tags='elimicación-exitosa')
    return redirect('programas')

def crear_objetivo(id, objetivo):
    # Aca estaba el problema, cuando creo un objeto sin la plantilla HTML no tengo que usar el 
    #ObjetivoForm (formulario), simplemente instancio el objeto con python
    nuevo_objetivo = Objetivos()
    nuevo_objetivo.programa = id
    nuevo_objetivo.nombre = objetivo

    # Guarda el objeto en la base de datos
    nuevo_objetivo.save()

    return JsonResponse({"success": True})

def lista_indicadores(request):
    # Estos son todos los id que tienen los tipos en la base de datos
    # Por esto no andaba, buscabamos por nombre o por un id que no era el correcto
    tipo_opciones = {
        "Eficacia": ["1", "2", "4"],
        "Eficiencia": ["3", "5", "8"],
        "Calidad": ["6"],
        "Economia": ["9"],
    }
    tipo = request.GET.get('tipo')
    ambito = request.GET.get('ambito')
    programa = request.GET.get('programa')
    frecuencia = request.GET.get('periodicidad')
    indicadores = Indicador.objects.all()

    if tipo:
        tipo = tipo_opciones[tipo]
        indicadores = indicadores.filter(tipo__in=tipo)
    if ambito:
        indicadores = indicadores.filter(ambito=ambito)
    if programa:
        indicadores = indicadores.filter(programa=programa)
    if frecuencia:
        indicadores = indicadores.filter(frecuencia=frecuencia)

    return render(request, 'indicadores/index.html', {'indicador': indicadores})