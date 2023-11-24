from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('error', views.error, name='error'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('tipos', views.tipos, name = "tipos"),
    path('get_chart', views.get_chart, name='get_chart'),
    path('valores', views.valores, name = "valores"),
    path('medidas', views.medidas, name = "medidas"),
    path('listar_metricas', views.listar_metricas, name = "listar_metricas"),
    path('crear_excel', views.crear_excel, name="crear_excel"),
    path('instancias', views.instancias, name = "instancias"),
    path('programas',views.programas, name='programas'),
    path('programas/crear',views.crear_programa, name='crear_programa'),
    path('programas/eliminar/<int:id>', views.eliminar_programas, name='eliminar_programas'),
    path('programas/editar/<int:id>', views.editar_programas, name='editar_programas'),
    path('indicadores',views.indicadores, name='indicadores'),
    path('indicadores/crear', views.crear_indicadores, name='crear_indicador'),
    path('indicadores/eliminar/<int:id>', views.eliminar_indicador, name='eliminar_indicador'),
    path('indicadores/editar/<int:id>', views.editar_indicadores, name='editar_indicador'),
    path('metricas', views.metricas, name='metricas'),
    path('metricas/crear', views.crear_metricas, name='crear'),
    path('metricas/editar/<int:id>', views.editar_metricas, name='editar'),
    path('metricas/eliminar/<int:id>', views.eliminar_metricas, name='eliminar'),
    path('historial-metrica/<int:metrica_id>/', views.historial_metrica, name='historial_metrica'),
    path('eliminar_historial_metrica/<int:historial_id>/', views.eliminar_historial_metrica, name='eliminar_historial_metrica'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)