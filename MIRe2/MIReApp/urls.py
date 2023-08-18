from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('metricas', views.metricas, name='metricas'),
    path('error', views.error, name='error'),
    path('metricas/crear', views.crear_metricas, name='crear'),
    path('metricas/editar/<int:id>', views.editar_metricas, name='editar'),
    path('metricas/eliminar/<int:id>', views.eliminar_metricas, name='eliminar'),
    path('historial-metrica/<int:metrica_id>/', views.historial_metrica, name='historial_metrica'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)