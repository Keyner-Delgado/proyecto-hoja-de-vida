from django.shortcuts import render
from .models import (
    DatosPersonales, ExperienciaLaboral, CursosRealizados, 
    Reconocimientos, ProductosAcademicos, ProductosLaborales, VentaGarage
)
from .models import ReporteUnificado, CursosRealizados, Reconocimientos # Asegúrate de importar tus modelos

def home(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'home.html', {'perfil': perfil})

def experiencia(request):
    perfil = DatosPersonales.objects.first()
    # Usamos idperfil=perfil para que Django busque los trabajos
    # asociados a ese objeto de perfil específico.
    items = ExperienciaLaboral.objects.filter(idperfil=perfil)
    return render(request, 'experiencia.html', {'perfil': perfil, 'items': items})

def cursos(request):
    perfil = DatosPersonales.objects.first()
    # Filtramos los cursos por el perfil activo
    items = CursosRealizados.objects.filter(idperfil=perfil)
    
    # AGREGAR ESTA LÍNEA: Es la que busca el PDF en la Sección 8
    reporte = ReporteUnificado.objects.filter(tipo='CURSOS').first()
    
    return render(request, 'cursos.html', {
        'perfil': perfil, 
        'items': items, 
        'reporte_cursos': reporte  # Enviamos el archivo al HTML
    })

def reconocimientos(request):
    perfil = DatosPersonales.objects.first()
    # Filtramos los reconocimientos por perfil
    items = Reconocimientos.objects.filter(idperfil=perfil)
    # BUSCAMOS EL REPORTE AQUÍ
    reporte = ReporteUnificado.objects.filter(tipo='RECONOCIMIENTOS').first()
    
    return render(request, 'reconocimientos.html', {
        'perfil': perfil, 
        'items': items, 
        'reporte_premios': reporte
    })

def productos_academicos(request):
    perfil = DatosPersonales.objects.first()
    # Filtramos por el perfil activo
    items = ProductosAcademicos.objects.filter(idperfil=perfil)
    return render(request, 'productos_academicos.html', {'perfil': perfil, 'items': items})

def productos_laborales(request):
    perfil = DatosPersonales.objects.first()
    items = ProductosLaborales.objects.filter(idperfil=perfil)
    return render(request, 'productos_laborales.html', {'perfil': perfil, 'items': items})

def garage(request):
    perfil = DatosPersonales.objects.first()
    # Filtramos los objetos de la venta de garage para este perfil
    items = VentaGarage.objects.filter(idperfil=perfil)
    return render(request, 'garage.html', {'perfil': perfil, 'items': items})
# El resto de tus funciones (cursos, reconocimientos, etc.) 
# están bien con esa misma estructura.

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Importamos todos los modelos que me pasaste
from .models import (
    DatosPersonales, 
    ExperienciaLaboral, 
    ProductosAcademicos, 
    CursosRealizados, 
    Reconocimientos, 
    ProductosLaborales
)

def pdf_datos_personales(request):
    # 1. Obtenemos el perfil activo
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    
    # 2. Consultas vinculadas al perfil (usando el campo idperfil de tus modelos)
    experiencias = ExperienciaLaboral.objects.filter(idperfil=perfil)
    productos_academicos = ProductosAcademicos.objects.filter(idperfil=perfil)
    productos_laborales = ProductosLaborales.objects.filter(idperfil=perfil)
    cursos = CursosRealizados.objects.filter(idperfil=perfil)
    reconocimientos = Reconocimientos.objects.filter(idperfil=perfil)
    
    # 3. Configuración de la respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="CV_{perfil.apellidos}.pdf"'
    
    # 4. Cargamos la plantilla HTML
    template = get_template('reportes/pdf_personales.html')
    
    # 5. Definimos el CONTEXTO (Asegúrate de que los nombres coincidan con los del HTML)
    context = {
        'perfil': perfil,
        'items': experiencias,               # Mantenemos 'items' para no romper tu lógica original
        'productos': productos_academicos,
        'productos_laborales': productos_laborales,
        'cursos': cursos,
        'reconocimientos': reconocimientos,
    }
    
    # 6. Renderizamos la plantilla
    html = template.render(context)
    
    # 7. Generamos el PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # 8. Verificación de errores
    if pisa_status.err:
        return HttpResponse('Ocurrió un error al generar el PDF', status=500)
    
    return response

